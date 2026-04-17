import textwrap
from pathlib import Path

from conan.tools.build.cpu import build_jobs
from jinja2 import Template

from conan.errors import ConanException
from conan.tools.files import save
from conan.tools.microsoft.msbuild import MSBuild
from conan.tools.premake.toolchain import PremakeToolchain
from conan.tools.premake.constants import CONAN_TO_PREMAKE_ARCH

# Source: https://learn.microsoft.com/en-us/cpp/overview/compiler-versions?view=msvc-170
PREMAKE_VS_VERSION = {
    '190': '2015',
    '191': '2017',
    '192': '2019',
    '193': '2022',
    '194': '2022',  # still 2022
    '195': '2026'
}


class Premake:
    """
    This class calls Premake commands when a package is being built. Notice that
    this one should be used together with the ``PremakeToolchain`` generator.

    This premake generator is only compatible with ``premake5``.
    """

    filename = "conanfile.premake5.lua"

    # Conan premake file which will preconfigure toolchain and then will call the user's premake file
    _premake_file_template = textwrap.dedent(
        """\
    #!lua
    include("{{luafile}}")
    include("{{premake_conan_toolchain}}")
    """
    )

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        #: Path to the root premake5 lua file (default is ``premake5.lua``)
        self.luafile = (Path(self._conanfile.source_folder) / "premake5.lua").as_posix()
        #: Key value pairs. Will translate to "--{key}={value}"
        self.arguments = {}  # https://premake.github.io/docs/Command-Line-Arguments/

        if "msvc" in self._conanfile.settings.compiler:
            msvc_version = PREMAKE_VS_VERSION.get(str(self._conanfile.settings.compiler.version))
            self.action = f'vs{msvc_version}'
        else:
            self.action = "gmake"  # New generator (old gmakelegacy is deprecated)

        self._premake_conan_toolchain = Path(self._conanfile.generators_folder) / PremakeToolchain.filename

    @staticmethod
    def _expand_args(args):
        pass

    def configure(self):
        """
        Runs ``premake5 <action> [FILE]`` which will generate respective build scripts depending on the ``action``.
        """
        pass

    @property
    def _premake_verbosity(self):
        pass

    @property
    def _compilation_verbosity(self):
        pass

    def build(self, workspace, targets=None, configuration=None, msbuild_platform=None):
        """
        Depending on the action, this method will run either ``msbuild`` or ``make`` with ``N_JOBS``.
        You can specify ``N_JOBS`` through the configuration line ``tools.build:jobs=N_JOBS``
        in your profile ``[conf]`` section.

        :param workspace: ``str`` Specifies the solution to be compiled (only used by ``MSBuild``).
        :param targets: ``List[str]`` Declare the projects to be built (None to build all projects).
        :param configuration: ``str`` Specify the configuration build type, default to build_type ("Release" or "Debug"),
            but this allow setting custom configuration type.
        :param msbuild_platform: ``str`` Specify the platform for the internal MSBuild generator (only used by ``MSBuild``).
        """
        pass
