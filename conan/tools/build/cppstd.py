import operator

from conan.errors import ConanInvalidConfiguration, ConanException
from conan.internal.api.detect.detect_api import default_cppstd as default_cppstd_
from conan.internal.model.version import Version


def check_min_cppstd(conanfile, cppstd, gnu_extensions=False):
    """ Check if current cppstd fits the minimal version required.

        In case the current cppstd doesn't fit the minimal version required
        by cppstd, a ConanInvalidConfiguration exception will be raised.

        settings.compiler.cppstd must be defined, otherwise ConanInvalidConfiguration is raised

    :param conanfile: The current recipe object. Always use ``self``.
    :param cppstd: Minimal cppstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17)
    """
    pass


def check_max_cppstd(conanfile, cppstd, gnu_extensions=False):
    """ Check if current cppstd fits the maximum version required.

        In case the current cppstd doesn't fit the maximum version required
        by cppstd, a ConanInvalidConfiguration exception will be raised.

        settings.compiler.cppstd must be defined, otherwise ConanInvalidConfiguration is raised

    :param conanfile: The current recipe object. Always use ``self``.
    :param cppstd: Maximum cppstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17)
    """
    pass


def valid_min_cppstd(conanfile, cppstd, gnu_extensions=False):
    """ Validate if current cppstd fits the minimal version required.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cppstd: Minimal cppstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17). This option ONLY works on Linux.
    :return: True, if current cppstd matches the required cppstd version. Otherwise, False.
    """
    pass


def valid_max_cppstd(conanfile, cppstd, gnu_extensions=False):
    """ Validate if current cppstd fits the maximum version required.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cppstd: Maximum cppstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17). This option ONLY works on Linux.
    :return: True, if current cppstd matches the required cppstd version. Otherwise, False.
    """
    pass


def default_cppstd(conanfile, compiler=None, compiler_version=None):
    """
    Get the default ``compiler.cppstd`` for the "conanfile.settings.compiler" and "conanfile
    settings.compiler_version" or for the parameters "compiler" and "compiler_version" if specified.

    :param conanfile: The current recipe object. Always use ``self``.
    :param compiler: Name of the compiler e.g. gcc
    :param compiler_version: Version of the compiler e.g. 12
    :return: The default ``compiler.cppstd`` for the specified compiler
    """
    pass


def supported_cppstd(conanfile, compiler=None, compiler_version=None):
    """
    Get a list of supported ``compiler.cppstd`` for the "conanfile.settings.compiler" and
    "conanfile.settings.compiler_version" or for the parameters "compiler" and "compiler_version"
    if specified.

    :param conanfile: The current recipe object. Always use ``self``.
    :param compiler: Name of the compiler e.g: gcc
    :param compiler_version: Version of the compiler e.g: 12
    :return: a list of supported ``cppstd`` values.
    """
    pass


def _check_cppstd(conanfile, cppstd, comparator, gnu_extensions):
    """ Check if current cppstd fits the version required according to a given comparator.

        In case the current cppstd doesn't fit the maximum version required
        by cppstd, a ConanInvalidConfiguration exception will be raised.

        settings.compiler.cppstd must be defined, otherwise ConanInvalidConfiguration is raised

    :param conanfile: The current recipe object. Always use ``self``.
    :param cppstd: Required cppstd version.
    :param comparator: Operator to use to compare the detected and the required cppstd versions.
    :param gnu_extensions: GNU extension is required (e.g gnu17)
    """
    pass


def _apple_clang_supported_cppstd(version):
    """
    ["98", "gnu98", "11", "gnu11", "14", "gnu14", "17", "gnu17", "20", "gnu20"]
    """
    pass


def _gcc_supported_cppstd(version):
    """
    ["98", "gnu98", "11", "gnu11", "14", "gnu14", "17", "gnu17", "20", "gnu20", "23", "gnu23"]
    """
    pass


def _msvc_supported_cppstd(version):
    """
    https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version?view=msvc-170
    - /std:c++14 starting in Visual Studio 2015 Update 3 (190)
    - /std:c++17 starting in Visual Studio 2017 version 15.3. (191)
    - /std:c++20 starting in Visual Studio 2019 version 16.11 (192)
    [14, 17, 20, 23]
    """
    pass


def _clang_supported_cppstd(version):
    """
    ["98", "gnu98", "11", "gnu11", "14", "gnu14", "17", "gnu17", "20", "gnu20", "23", "gnu23"]
    """
    pass


def _mcst_lcc_supported_cppstd(version):
    """
    ["98", "gnu98", "11", "gnu11", "14", "gnu14", "17", "gnu17", "20", "gnu20", "23", "gnu23"]
    """
    pass


def _qcc_supported_cppstd(version):
    """
    [98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17]
    """
    pass


def _emcc_supported_cppstd(version):
    """
    emcc is based on clang but follow different versioning scheme.
    """
    pass
