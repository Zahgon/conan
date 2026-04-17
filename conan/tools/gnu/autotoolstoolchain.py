import os

from conan.errors import ConanException
from conan.internal import check_duplicated_generator
from conan.internal.internal_tools import is_universal_arch
from conan.tools.apple.apple import is_apple_os, resolve_apple_flags, apple_extra_flags
from conan.tools.build import cmd_args_to_string, save_toolchain_args
from conan.tools.build.cross_building import cross_building
from conan.tools.build.flags import architecture_flag, architecture_link_flag, build_type_flags, cppstd_flag, \
    build_type_link_flags, libcxx_flags, cstd_flag, llvm_clang_front, threads_flags
from conan.tools.env import Environment, VirtualBuildEnv
from conan.tools.gnu.get_gnu_triplet import _get_gnu_triplet
from conan.tools.microsoft import VCVars, msvc_runtime_flag, unix_path, check_min_vs, is_msvc
from conan.internal.model.pkg_type import PackageType


class AutotoolsToolchain:

    def __init__(self, conanfile, namespace=None, prefix="/"):
        """
        :param conanfile: The current recipe object. Always use ``self``.
        :param namespace: This argument avoids collisions when you have multiple toolchain calls in
               the same recipe. By setting this argument, the *conanbuild.conf* file used to pass
               information to the build helper will be named as *<namespace>_conanbuild.conf*. The default
               value is ``None`` meaning that the name of the generated file is *conanbuild.conf*. This
               namespace must be also set with the same value in the constructor of the Autotools build
               helper so that it reads the information from the proper file.
        :param prefix: Folder to use for ``--prefix`` argument ("/" by default).
        """

        self._conanfile = conanfile
        self._namespace = namespace
        self._prefix = prefix

        # Flags
        self.extra_cxxflags = []
        self.extra_cflags = []
        self.extra_ldflags = []
        self.extra_defines = []

        # Defines
        self.ndebug = None
        build_type = self._conanfile.settings.get_safe("build_type")
        if build_type in ['Release', 'RelWithDebInfo', 'MinSizeRel']:
            self.ndebug = "NDEBUG"

        # TODO: This is also covering compilers like Visual Studio, necessary to test it (&remove?)
        self.build_type_flags = build_type_flags(self._conanfile)
        self.build_type_link_flags = build_type_link_flags(self._conanfile.settings)

        self.cppstd = cppstd_flag(self._conanfile)
        self.cstd = cstd_flag(self._conanfile)
        self.arch_flag = architecture_flag(self._conanfile)
        self.arch_ld_flag = architecture_link_flag(self._conanfile)
        self.threads_flags = threads_flags(self._conanfile)
        self.libcxx, self.gcc_cxx11_abi = libcxx_flags(self._conanfile)
        self.fpic = self._conanfile.options.get_safe("fPIC")
        self.msvc_runtime_flag = self._get_msvc_runtime_flag()
        self.msvc_extra_flags = self._msvc_extra_flags()
        self.msvc_runtime_link_flags = []
        if llvm_clang_front(self._conanfile) == "clang":
            self.msvc_runtime_link_flags = ["-fuse-ld=lld-link"]

        self._is_universal_arch = is_universal_arch(conanfile.settings.get_safe("arch"),
                                                    conanfile.settings.possible_values().get("arch"))
        if self._is_universal_arch and not is_apple_os(self._conanfile):
            arch_str = conanfile.settings.get_safe('arch')
            raise ConanException(f"Universal arch '{arch_str}' is only supported in Apple OSes")

        # Cross build triplets
        self._host = self._conanfile.conf.get("tools.gnu:host_triplet")
        self._build = self._conanfile.conf.get("tools.gnu:build_triplet")
        self._target = None

        self.android_cross_flags = {}
        self._is_cross_building = not self._is_universal_arch and cross_building(self._conanfile)
        if self._is_cross_building:
            compiler = self._conanfile.settings.get_safe("compiler")
            # If cross-building and tools.android:ndk_path is defined, let's try to guess the Android
            # cross-building flags
            self.android_cross_flags = self._resolve_android_cross_compilation()
            # If it's not defined the triplet
            if not self._host:
                os_host = conanfile.settings.get_safe("os")
                arch_host = conanfile.settings.get_safe("arch")
                self._host = _get_gnu_triplet(os_host, arch_host, compiler=compiler)["triplet"]
            # Build triplet
            if not self._build:
                os_build = conanfile.settings_build.get_safe('os')
                arch_build = conanfile.settings_build.get_safe('arch')
                self._build = _get_gnu_triplet(os_build, arch_build, compiler=compiler)["triplet"]

        sysroot = self._conanfile.conf.get("tools.build:sysroot")
        if sysroot:
            root = sysroot.replace("\\", "/")
            compiler = self._conanfile.settings.get_safe("compiler")
            self.sysroot_flag = f"--sysroot {root}" if compiler != "qcc" else f"-Wc,-isysroot,{root}"
        else:
            self.sysroot_flag = None

        extra_configure_args = self._conanfile.conf.get("tools.gnu:extra_configure_args",
                                                        check_type=list,
                                                        default=[])

        self.configure_args = (self._default_configure_shared_flags() +
                               self._default_configure_install_flags() +
                               self._get_triplets() +
                               extra_configure_args)
        self.autoreconf_args = self._default_autoreconf_flags()
        self.make_args = []
        # Apple stuff
        is_cross_building_osx = (self._is_cross_building
                                 and conanfile.settings_build.get_safe('os') == "Macos"
                                 and is_apple_os(conanfile)
                                 and not self._is_universal_arch)

        min_flag, arch_flags, isysroot_flag = (
            resolve_apple_flags(conanfile, is_cross_building=is_cross_building_osx,
                                is_universal=self._is_universal_arch)
        )
        # https://man.archlinux.org/man/clang.1.en#Target_Selection_Options
        self.apple_arch_flag = arch_flags
        # -isysroot makes all includes for your library relative to the build directory
        self.apple_isysroot_flag = isysroot_flag
        self.apple_min_version_flag = min_flag
        self.apple_extra_flags = apple_extra_flags(self._conanfile)

    def _resolve_android_cross_compilation(self):
        # Issue related: https://github.com/conan-io/conan/issues/13443
        pass

    def _get_msvc_runtime_flag(self):
        pass

    def _msvc_extra_flags(self):
        pass

    def _add_msvc_flags(self, flags):
        # This is to avoid potential duplicate with users recipes -FS (already some in ConanCenter)
        pass

    @staticmethod
    def _filter_list_empty_fields(v):
        pass

    @property
    def cxxflags(self):
        pass

    @property
    def cflags(self):
        pass

    @property
    def ldflags(self):
        pass

    @property
    def defines(self):
        pass

    @property
    def rcflags(self):
        pass

    def _include_obj_arc_flags(self, env):
        pass

    def environment(self):
        pass

    def vars(self):
        pass

    def generate(self, env=None, scope="build"):
        pass

    def _default_configure_shared_flags(self):
        pass

    def _default_configure_install_flags(self):
        pass

    @staticmethod
    def _default_autoreconf_flags():
        pass

    def _get_triplets(self):
        pass

    def update_configure_args(self, updated_flags):
        """
        Helper to update/prune flags from ``self.configure_args``.

        :param updated_flags: ``dict`` with arguments as keys and their argument values.
                              Notice that if argument value is ``None``, this one will be pruned.
        """
        pass

    def update_make_args(self, updated_flags):
        """
        Helper to update/prune arguments from ``self.make_args``.

        :param updated_flags: ``dict`` with arguments as keys and their argument values.
                              Notice that if argument value is ``None``, this one will be pruned.
        """
        pass

    def update_autoreconf_args(self, updated_flags):
        """
        Helper to update/prune arguments from ``self.autoreconf_args``.

        :param updated_flags: ``dict`` with arguments as keys and their argument values.
                              Notice that if argument value is ``None``, this one will be pruned.
        """
        pass

    # FIXME: Remove all these update_xxxx whenever xxxx_args are dicts or new ones replace them
    def _update_flags(self, attr_name, updated_flags):

        pass

    def generate_args(self):
        pass
