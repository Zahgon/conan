from conan.errors import ConanException
from conan.tools.microsoft.visual import msvc_platform_from_arch


def msbuild_verbosity_cmd_line_arg(conanfile):
    """
    Controls msbuild verbosity.
    See https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference
    :return:
    """
    pass


class MSBuild:
    """
    MSBuild build helper class
    """

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        #: Defines the build type. By default, ``settings.build_type``.
        self.build_type = conanfile.settings.get_safe("build_type")
        # if platforms:
        #    msvc_arch.update(platforms)
        arch = conanfile.settings.get_safe("arch")
        # MSVC default platform for VS projects is "x86", not "Win32" (but CMake default is "Win32")
        msvc_platform = msvc_platform_from_arch(arch) if arch != "x86" else "x86"
        if conanfile.settings.get_safe("os") == "WindowsCE":
            msvc_platform = conanfile.settings.get_safe("os.platform")
        #: Defines the platform name, e.g., ``ARM`` if ``settings.arch == "armv7"``.
        self.platform = msvc_platform

    def command(self, sln, targets=None):
        """
        Gets the ``msbuild`` command line. For instance,
        :command:`msbuild.exe "MyProject.sln" -p:Configuration=<conf> -p:Platform=<platform>`.

        :param sln: ``str`` name of Visual Studio ``*.sln`` file
        :param targets: ``targets`` is an optional argument, defaults to ``None``, and otherwise it is a list of targets to build
        :return: ``str`` msbuild command line.
        """
        pass

    def build(self, sln, targets=None):
        """
        Runs the ``msbuild`` command line obtained from ``self.command(sln)``.

        :param sln: ``str`` name of Visual Studio ``*.sln`` file
        :param targets: ``targets`` is an optional argument, defaults to ``None``, and otherwise it is a list of targets to build
        """
        pass

    @staticmethod
    def get_version(_):
        pass
