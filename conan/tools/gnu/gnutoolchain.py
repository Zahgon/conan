import os

from conan.errors import ConanException
from conan.internal import check_duplicated_generator
from conan.internal.internal_tools import is_universal_arch
from conan.tools.apple.apple import is_apple_os, resolve_apple_flags, apple_extra_flags
from conan.tools.build import cmd_args_to_string, save_toolchain_args
from conan.tools.build.cross_building import cross_building
from conan.tools.build.flags import architecture_flag, architecture_link_flag, build_type_flags, cppstd_flag, \
    build_type_link_flags, \
    libcxx_flags, llvm_clang_front, threads_flags
from conan.tools.env import Environment, VirtualBuildEnv
from conan.tools.gnu.get_gnu_triplet import _get_gnu_triplet
from conan.tools.microsoft import VCVars, msvc_runtime_flag, unix_path, check_min_vs, is_msvc
from conan.internal.model.pkg_type import PackageType


class GnuToolchain:
    """
    GnuToolchain generator.

    Note: it's based on legacy AutotoolsToolchain but with a more modern and usable UX
    """
    script_name = "conangnutoolchain"

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
        self._is_apple_system = is_apple_os(self._conanfile)
        self._prefix = prefix
        # Extra flags
        self.extra_cxxflags = []
        self.extra_cflags = []
        self.extra_ldflags = []
        self.extra_defines = []
        # Extra environment definitions
        self.extra_env = Environment()
        # Defines
        self.ndebug = None
        build_type = self._conanfile.settings.get_safe("build_type")
        if build_type in ['Release', 'RelWithDebInfo', 'MinSizeRel']:
            self.ndebug = "NDEBUG"

        # TODO: This is also covering compilers like Visual Studio, necessary to test it (&remove?)
        self.build_type_flags = build_type_flags(self._conanfile)
        self.build_type_link_flags = build_type_link_flags(self._conanfile.settings)

        self.cppstd = cppstd_flag(self._conanfile)
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

        extra_configure_args = self._conanfile.conf.get("tools.gnu:extra_configure_args",
                                                        check_type=list,
                                                        default=[])
        extra_configure_args = {it: None for it in extra_configure_args}

        # Host/Build triplets
        self.triplets_info = {
            "host": {"triplet": self._conanfile.conf.get("tools.gnu:host_triplet")},
            "build": {"triplet": self._conanfile.conf.get("tools.gnu:build_triplet")}
        }
        self._is_cross_building = not self._is_universal_arch and cross_building(self._conanfile)
        if self._is_cross_building:
            compiler = self._conanfile.settings.get_safe("compiler")
            # Host triplet
            if not self.triplets_info["host"]["triplet"]:
                os_host = conanfile.settings.get_safe("os")
                arch_host = conanfile.settings.get_safe("arch")
                self.triplets_info["host"] = _get_gnu_triplet(os_host, arch_host, compiler=compiler)
            # Build triplet
            if not self.triplets_info["build"]["triplet"]:
                os_build = conanfile.settings_build.get_safe('os')
                arch_build = conanfile.settings_build.get_safe('arch')
                self.triplets_info["build"] = _get_gnu_triplet(os_build, arch_build, compiler=compiler)

        sysroot = self._conanfile.conf.get("tools.build:sysroot")
        if sysroot:
            root = sysroot.replace("\\", "/")
            compiler = self._conanfile.settings.get_safe("compiler")
            self.sysroot_flag = f"--sysroot {root}" if compiler != "qcc" else f"-Wc,-isysroot,{root}"
        else:
            self.sysroot_flag = None

        self.configure_args = {}
        self.autoreconf_args = {"--force": None, "--install": None}
        self.make_args = {}
        # Initializing configure arguments: triplets, shared flags, dirs flags, etc.
        self.configure_args.update(self._get_default_configure_shared_flags())
        self.configure_args.update(self._get_default_configure_install_flags())
        self.configure_args.update(self._get_default_triplets())
        self.configure_args.update(extra_configure_args)
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
        self.apple_extra_flags = apple_extra_flags(conanfile)
        # Default initial environment flags
        self._initialize_default_extra_env()

    def yes_no(self, option_name, default=None, negated=False):
        """
        Simple wrapper to return "yes" or "no" depending on whether option_name is
        evaluated as True or False.

        :param option_name: option name.
        :param default: Default value to return.
        :param negated: Negates the option value if True.
        :return: "yes" or "no" depending on whether option_name is True or False.
        """
        pass

    def _resolve_android_cross_compilation(self):
        # Issue related: https://github.com/conan-io/conan/issues/13443
        pass

    def _resolve_compilers_mapping_variables(self):
        pass

    def _initialize_default_extra_env(self):
        """Initialize the default environment variables."""
        pass

    def _get_msvc_runtime_flag(self):
        pass

    def _msvc_extra_flags(self):
        pass

    def _add_msvc_flags(self, flags):
        # This is to avoid potential duplicate with users recipes -FS (alreday some in ConanCenter)
        pass

    @staticmethod
    def _filter_list_empty_fields(v):
        pass

    @staticmethod
    def _dict_to_list(flags):
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

    def _get_default_configure_shared_flags(self):
        pass

    def _get_default_configure_install_flags(self):
        pass

    def _get_default_triplets(self):
        pass

    def _include_obj_arc_flags(self, env):
        pass

    @property
    def _environment(self):
        pass

    def generate(self):
        pass
