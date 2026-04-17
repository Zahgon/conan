import os
import textwrap

from conan.api.output import ConanOutput
from conan.internal import check_duplicated_generator
from conan.internal.api.detect.detect_vs import vs_installation_path
from conan.errors import ConanException, ConanInvalidConfiguration
from conan.tools.scm import Version
from conan.tools.intel.intel_cc import IntelCC
from conan.internal.util.files import save

CONAN_VCVARS = "conanvcvars"


def msvc_platform_from_arch(arch):
    pass


def check_min_vs(conanfile, version, raise_invalid=True):
    """
    This is a helper method to allow the migration of 1.X -> 2.0 and VisualStudio -> msvc settings
    without breaking recipes.
    The legacy "Visual Studio" with different toolset is not managed, not worth the complexity.

    :param raise_invalid: ``bool`` Whether to raise or return False if the version check fails
    :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
    :param version: ``str`` Visual Studio or msvc version number.
    """
    pass


def msvc_version_to_vs_ide_version(version):
    """
    Gets the Visual Studio IDE version given the ``msvc`` compiler one.

    :param version: ``str`` or ``int`` msvc version
    :return: VS IDE version
    """
    pass


def msvc_version_to_toolset_version(version):
    """
    Gets the Visual Studio IDE toolset version given the ``msvc`` compiler one.

    :param version: ``str`` or ``int`` msvc version
    :return: VS IDE toolset version
    """
    pass


class VCVars:
    """
    VCVars class generator to generate a ``conanvcvars.bat`` script that activates the correct
    Visual Studio prompt.

    This generator will be automatically called by other generators such as ``CMakeToolchain``
    when considered necessary, for example if building with Visual Studio compiler using the
    CMake ``Ninja`` generator, which needs an active Visual Studio prompt.
    Then, it is not necessary to explicitly instantiate this generator in most cases.
    """

    def __init__(self, conanfile):
        """
        :param conanfile: ``ConanFile object`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile

    def generate(self, scope="build"):
        """
        Creates a ``conanvcvars.bat`` file that calls Visual ``vcvars`` with the necessary
        args to activate the correct Visual Studio prompt matching the Conan settings.

        :param scope: ``str`` activation scope, by default "build". It means it will add a
                      call to this ``conanvcvars.bat`` from the aggregating general
                      ``conanbuild.bat``, which is the script that will be called by default
                      in ``self.run()`` calls and build helpers such as ``cmake.configure()``
                      and ``cmake.build()``.
        """
        pass


def _create_deactivate_vcvars_file(conanfile, filename):
    pass


def vs_ide_version(conanfile):
    """
    Gets the VS IDE version as string. It'll use the ``compiler.version`` (if exists) and/or the
    ``tools.microsoft.msbuild:vs_version`` if ``compiler`` is ``msvc``.

    :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
    :return: ``str`` Visual IDE version number.
    """
    pass


def msvc_runtime_flag(conanfile):
    """
    Gets the MSVC runtime flag given the ``compiler.runtime`` value from the settings.

    :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
    :return: ``str`` runtime flag.
    """
    pass


def vcvars_command(version, architecture=None, platform_type=None, winsdk_version=None,
                   vcvars_ver=None, start_dir_cd=True, vs_install_path=None):
    """
    Conan-agnostic construction of vcvars command
    https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line

    :param version: ``str`` Visual Studio version.
    :param architecture: ``str`` Specifies the host and target architecture to use.
    :param platform_type: ``str`` Allows you to specify ``store`` or ``uwp`` as the platform type.
    :param winsdk_version: ``str`` Specifies the version of the Windows SDK to use.
    :param vcvars_ver: ``str`` Specifies the Visual Studio compiler toolset to use.
    :param start_dir_cd: ``bool`` If ``True``, the command will execute
                         ``set "VSCMD_START_DIR=%CD%`` at first.
    :param vs_install_path: ``str`` Visual Studio installation path.
    :return: ``str`` complete _vcvarsall_ command.
    """
    pass


def _vcvars_path(version, vs_install_path):
    # TODO: This comes from conans/client/tools/win.py vcvars_command()
    pass


def _vcvars_versions(conanfile):
    pass


def _vcvars_arch(conanfile):
    """
    Computes the vcvars command line architecture based on conanfile settings (host) and
    settings_build.
    """
    pass


def is_msvc(conanfile, build_context=False):
    """
    Validates if the current compiler is ``msvc``.

    :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
    :param build_context: If True, will use the settings from the build context, not host ones
    :return: ``bool`` True, if the host compiler is ``msvc``, otherwise, False.
    """
    pass


def is_msvc_static_runtime(conanfile):
    """
    Validates when building with Visual Studio or msvc and MT on runtime.

    :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
    :return: ``bool`` True, if ``msvc + runtime MT``. Otherwise, False.
    """
    pass


def msvs_toolset(conanfile):
    """
    Returns the corresponding platform toolset based on the compiler setting.
    In case no toolset is configured in the profile, it will return a toolset based on the
    compiler version, otherwise, it will return the toolset from the profile.
    When there is no compiler version neither toolset configured, it will return None
    It supports msvc, intel-cc and clang compilers. For clang, is assumes the ClangCl toolset,
    as provided by the Visual Studio installer.

    :param conanfile: Conanfile instance to access settings.compiler
    :return: A toolset when compiler.version is valid or compiler.toolset is configured. Otherwise, None.
    """
    pass
