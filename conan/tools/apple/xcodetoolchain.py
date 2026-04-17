import textwrap

from conan.internal import check_duplicated_generator
from conan.tools.apple.apple import to_apple_arch, xcodebuild_deployment_target_key
from conan.tools.apple.xcodedeps import GLOBAL_XCCONFIG_FILENAME, GLOBAL_XCCONFIG_TEMPLATE, \
    _add_includes_to_file_or_create, _xcconfig_settings_filename, _xcconfig_conditional
from conan.internal.util.files import save


class XcodeToolchain:
    filename = "conantoolchain"
    extension = ".xcconfig"

    _vars_xconfig = textwrap.dedent("""\
        // Definition of toolchain variables
        {apple_deployment_target}
        {clang_cxx_library}
        {clang_cxx_language_standard}
        """)

    _flags_xconfig = textwrap.dedent("""\
        // Global flags
        {defines}
        {cflags}
        {cppflags}
        {ldflags}
        """)

    _agreggated_xconfig = textwrap.dedent("""\
        // Conan XcodeToolchain generated file
        // Includes all installed configurations

        """)

    def __init__(self, conanfile):
        self._conanfile = conanfile
        arch = conanfile.settings.get_safe("arch")
        self.architecture = to_apple_arch(self._conanfile, default=arch)
        self.configuration = conanfile.settings.build_type
        self.libcxx = conanfile.settings.get_safe("compiler.libcxx")
        self.os_version = conanfile.settings.get_safe("os.version")
        self._global_defines = self._conanfile.conf.get("tools.build:defines", default=[], check_type=list)
        self._global_cxxflags = self._conanfile.conf.get("tools.build:cxxflags", default=[], check_type=list)
        self._global_cflags = self._conanfile.conf.get("tools.build:cflags", default=[], check_type=list)
        sharedlinkflags = self._conanfile.conf.get("tools.build:sharedlinkflags", default=[], check_type=list)
        exelinkflags = self._conanfile.conf.get("tools.build:exelinkflags", default=[], check_type=list)
        self._global_ldflags = sharedlinkflags + exelinkflags

    def generate(self):
        pass

    @property
    def _cppstd(self):
        pass

    @property
    def _apple_deployment_target(self):
        pass

    @property
    def _clang_cxx_library(self):
        pass

    @property
    def _clang_cxx_language_standard(self):
        pass

    @property
    def _vars_xconfig_filename(self):
        pass

    @property
    def _vars_xconfig_content(self):
        pass

    @property
    def _agreggated_xconfig_content(self):
        pass

    @property
    def _global_xconfig_content(self):
        pass

    @property
    def _agreggated_xconfig_filename(self):
        pass

    @property
    def _check_if_extra_flags(self):
        pass

    @property
    def _flags_xcconfig_content(self):
        pass

    @property
    def _flags_xcconfig_filename(self):
        pass
