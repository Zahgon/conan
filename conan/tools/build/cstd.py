import operator

from conan.errors import ConanInvalidConfiguration, ConanException
from conan.internal.api.detect.detect_api import default_cstd as default_cstd_
from conan.internal.model.version import Version


def check_min_cstd(conanfile, cstd, gnu_extensions=False):
    """ Check if current cstd fits the minimal version required.

        In case the current cstd doesn't fit the minimal version required
        by cstd, a ConanInvalidConfiguration exception will be raised.

        1. If settings.compiler.cstd, the tool will use settings.compiler.cstd to compare
        2. It not settings.compiler.cstd, the tool will use compiler to compare (reading the
           default from cstd_default)
        3. If not settings.compiler is present (not declared in settings) will raise because it
           cannot compare.
        4. If can not detect the default cstd for settings.compiler, a exception will be raised.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cstd: Minimal cstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17)
    """
    pass


def check_max_cstd(conanfile, cstd, gnu_extensions=False):
    """ Check if current cstd fits the maximum version required.

        In case the current cstd doesn't fit the maximum version required
        by cstd, a ConanInvalidConfiguration exception will be raised.

        1. If settings.compiler.cstd, the tool will use settings.compiler.cstd to compare
        2. It not settings.compiler.cstd, the tool will use compiler to compare (reading the
           default from cstd_default)
        3. If not settings.compiler is present (not declared in settings) will raise because it
           cannot compare.
        4. If can not detect the default cstd for settings.compiler, a exception will be raised.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cstd: Maximum cstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17)
    """
    pass


def valid_min_cstd(conanfile, cstd, gnu_extensions=False):
    """ Validate if current cstd fits the minimal version required.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cstd: Minimal cstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17). This option ONLY works on Linux.
    :return: True, if current cstd matches the required cstd version. Otherwise, False.
    """
    pass


def valid_max_cstd(conanfile, cstd, gnu_extensions=False):
    """ Validate if current cstd fits the maximum version required.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cstd: Maximum cstd version required
    :param gnu_extensions: GNU extension is required (e.g gnu17). This option ONLY works on Linux.
    :return: True, if current cstd matches the required cstd version. Otherwise, False.
    """
    pass


def default_cstd(conanfile, compiler=None, compiler_version=None):
    """
    Get the default ``compiler.cstd`` for the "conanfile.settings.compiler" and "conanfile
    settings.compiler_version" or for the parameters "compiler" and "compiler_version" if specified.

    :param conanfile: The current recipe object. Always use ``self``.
    :param compiler: Name of the compiler e.g. gcc
    :param compiler_version: Version of the compiler e.g. 12
    :return: The default ``compiler.cstd`` for the specified compiler
    """
    pass


def supported_cstd(conanfile, compiler=None, compiler_version=None):
    """
    Get a list of supported ``compiler.cstd`` for the "conanfile.settings.compiler" and
    "conanfile.settings.compiler_version" or for the parameters "compiler" and "compiler_version"
    if specified.

    :param conanfile: The current recipe object. Always use ``self``.
    :param compiler: Name of the compiler e.g: gcc
    :param compiler_version: Version of the compiler e.g: 12
    :return: a list of supported ``cstd`` values.
    """
    pass


def _check_cstd(conanfile, cstd, comparator, gnu_extensions):
    """ Check if current cstd fits the version required according to a given comparator.

        In case the current cstd doesn't fit the maximum version required
        by cstd, a ConanInvalidConfiguration exception will be raised.

        1. If settings.compiler.cstd, the tool will use settings.compiler.cstd to compare
        2. It not settings.compiler.cstd, the tool will use compiler to compare (reading the
           default from cstd_default)
        3. If not settings.compiler is present (not declared in settings) will raise because it
           cannot compare.
        4. If can not detect the default cstd for settings.compiler, a exception will be raised.

    :param conanfile: The current recipe object. Always use ``self``.
    :param cstd: Required cstd version.
    :param comparator: Operator to use to compare the detected and the required cstd versions.
    :param gnu_extensions: GNU extension is required (e.g gnu17)
    """
    pass


def _apple_clang_supported_cstd(version):
    # TODO: Per-version support
    pass


def _gcc_supported_cstd(version):
    pass


def _msvc_supported_cstd(version):
    pass


def _clang_supported_cstd(version):
    pass


def _emcc_supported_cstd(version):
    """
    emcc is based on clang but follow different versioning scheme.
    """
    pass


