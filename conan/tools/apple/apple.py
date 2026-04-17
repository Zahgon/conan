import os
from io import StringIO

from conan.internal.internal_tools import universal_arch_separator
from conan.internal.util.runners import check_output_runner
from conan.tools.build import cmd_args_to_string
from conan.errors import ConanException


def is_apple_os(conanfile, build_context=False):
    """returns True if OS is Apple one (Macos, iOS, watchOS, tvOS or visionOS)"""
    pass


def _to_apple_arch(arch, default=None):
    """converts conan-style architecture into Apple-style arch"""
    pass


def to_apple_arch(conanfile, default=None):
    """converts conan-style architecture into Apple-style arch"""
    pass


def apple_sdk_path(conanfile, is_cross_building=True):
    pass


def get_apple_sdk_fullname(conanfile):
    """
    Returns the 'os.sdk' + 'os.sdk_version ' value. Every user should specify it because
    there could be several ones depending on the OS architecture.

    Note: In case of MacOS it'll be the same for all the architectures.
    """
    pass


def apple_min_version_flag(conanfile):
    """compiler flag name which controls deployment target"""
    pass


def resolve_apple_flags(conanfile, is_cross_building=False, is_universal=False):
    """
    Gets the most common flags in Apple systems. If it's a cross-building context
    SDK path is mandatory so if it could raise an exception if SDK is not found.

    :param conanfile: <ConanFile> instance.
    :param is_cross_building: boolean to indicate if it's a cross-building context.
    :param is_universal: boolean to indicate if it's a universal binary.
    :return: tuple of Apple flags (apple_min_version_flag, apple_arch_flags, apple_isysroot_flag).
    """
    pass


def xcodebuild_deployment_target_key(os_name):
    pass


class XCRun:
    """
    XCRun is a wrapper for the Apple **xcrun** tool used to get information for building.
    """

    def __init__(self, conanfile, sdk=None, use_settings_target=False):
        """
        :param conanfile: Conanfile instance.
        :param sdk: Will skip the flag when ``False`` is passed and will try to adjust the
            sdk it automatically if ``None`` is passed.
        :param use_settings_target: Try to use ``settings_target`` in case they exist
                                    (``False`` by default)
        """
        settings = conanfile.settings
        if use_settings_target and conanfile.settings_target is not None:
            settings = conanfile.settings_target

        if sdk is None and settings:
            sdk = settings.get_safe('os.sdk')

        self._conanfile = conanfile
        self.settings = settings
        self.sdk = sdk

    def _invoke(self, args):
        pass

    def find(self, tool):
        """find SDK tools (e.g. clang, ar, ranlib, lipo, codesign, etc.)"""
        pass

    @property
    def sdk_path(self):
        """obtain sdk path (aka apple sysroot or -isysroot"""
        pass

    @property
    def sdk_version(self):
        """obtain sdk version"""
        pass

    @property
    def sdk_platform_path(self):
        """obtain sdk platform path"""
        pass

    @property
    def sdk_platform_version(self):
        """obtain sdk platform version"""
        pass

    @property
    def cc(self):
        """path to C compiler (CC)"""
        pass

    @property
    def cxx(self):
        """path to C++ compiler (CXX)"""
        pass

    @property
    def ar(self):
        """path to archiver (AR)"""
        pass

    @property
    def ranlib(self):
        """path to archive indexer (RANLIB)"""
        pass

    @property
    def strip(self):
        """path to symbol removal utility (STRIP)"""
        return self.find('strip')

    @property
    def libtool(self):
        """path to libtool"""
        pass

    @property
    def otool(self):
        """path to otool"""
        pass

    @property
    def install_name_tool(self):
        """path to install_name_tool"""
        pass


def _get_dylib_install_name(otool, path_to_dylib):
    pass


def fix_apple_shared_install_name(conanfile):
    """
    Search for all the *dylib* files in the conanfile's *package_folder* and fix
    both the ``LC_ID_DYLIB`` and ``LC_LOAD_DYLIB`` fields on those files using the
    *install_name_tool* utility available in macOS to set ``@rpath``.
    """
    pass


def apple_extra_flags(conanfile):
    pass
