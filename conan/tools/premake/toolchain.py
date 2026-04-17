from conan.tools.build.flags import architecture_flag, architecture_link_flag, libcxx_flags, threads_flags
import os
import textwrap
from pathlib import Path

from conan.tools.env.virtualbuildenv import VirtualBuildEnv
from jinja2 import Template

from conan.tools.build.cross_building import cross_building
from conan.tools.files import save
from conan.tools.microsoft.visual import VCVars
from conan.tools.premake.premakedeps import PREMAKE_ROOT_FILE


def _generate_flags(self, conanfile):
    pass


class _PremakeProject:
    _premake_project_template = textwrap.dedent(
        """\
    project "{{ name }}"
        {% if kind %}
        kind "{{ kind }}"
        {% endif %}
        {% if flags %}
    {{ flags | indent(indent_level, first=True) }}
        {% endif %}
    """
    )

    def __init__(self, name, conanfile) -> None:
        self.name = name
        self.kind = None
        self.extra_cxxflags = []
        self.extra_cflags = []
        self.extra_ldflags = []
        self.extra_defines = []
        self.disable = False
        self._conanfile = conanfile

    def _generate(self):
        """Generates project block"""
        pass


class PremakeToolchain:
    """
    PremakeToolchain generator
    """

    filename = "conantoolchain.premake5.lua"
    # Keep template indented correctly for Lua output
    _premake_file_template = textwrap.dedent(
        """\
    #!lua
    -- Conan auto-generated toolchain file
    {% if has_conan_deps %}
    -- Include conandeps.premake5.lua with Conan dependency setup
    include("conandeps.premake5.lua")
    {% endif %}

    -- Base build directory
    local locationDir = path.normalize("{{ build_folder }}")

    -- Generate workspace configurations
    for wks in premake.global.eachWorkspace() do
        workspace(wks.name)
            -- Set base location for all workspaces
            location(locationDir)
            targetdir(path.join(locationDir, "bin"))
            objdir(path.join(locationDir, "obj"))

            {% if cppstd %}
            cppdialect "{{ cppstd }}"
            {% endif %}
            {% if cstd %}
            cdialect "{{ cstd }}"
            {% endif %}
            {% if shared != None %}
            -- IMPORTANT: this global setting will only apply `project`s which do not have `kind` set.
            -- IMPORTANT: This will not override existing `kind` set in `project` block.
            -- To let conan take control over `kind` of the libraries, DO NOT SET `kind` (StaticLib or
            -- SharedLib) in `project` block.
            kind "{{ "SharedLib" if shared else "StaticLib" }}"
            {% endif %}
            {% if fpic != None %}
            -- Enable position independent code
            pic "{{ "On" if fpic else "Off" }}"
            {% endif %}
            filter { "architecture: not wasm64" }
                -- TODO: There is an issue with premake and "wasm64" when system is declared "emscripten"
                system "{{ target_build_os }}"
            filter {}
            {% if macho_to_amd64 %}
            -- TODO: this should be fixed by premake: https://github.com/premake/premake-core/issues/2136
            buildoptions "-arch x86_64"
            linkoptions "-arch x86_64"
            {% endif %}
            {% if target_build_os == "emscripten" %}
            filter { "system:emscripten", "kind:ConsoleApp or WindowedApp" }
                -- Replace built in .wasm extension to .js to generate also a JavaScript files
                targetextension ".js"
            filter {}
            {% endif %}
            {% if flags %}
    {{ flags | indent(indent_level, first=True) }}
            {% endif %}

            filter { "system:macosx" }
                -- SHARED LIBS
                -- In the future we could add an opt in configuration to run
                -- fix_apple_shared_install_name on executables to have a similar behavior as CMake
                -- generator. Premake does not allow adding absolute RCPATHS
                -- Due to this limitation, if a consumer depends on a premake shared recipe, it will
                -- require to run conanrun script to setup proper DYLD_LIBRARY_PATH
                -- Reference: https://github.com/premake/premake-core/issues/2262#issuecomment-2378250385
                linkoptions { "-Wl,-rpath,@loader_path" }
            filter {}

            conan_setup()
    end

        {% for project in projects.values() %}

    {{ project._generate() }}
        {% endfor %}
    """
    )

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        self._projects = {}
        # Extra flags
        #: List of extra ``CXX`` flags. Added to ``buildoptions``.
        self.extra_cxxflags = []
        #: List of extra ``C`` flags. Added to ``buildoptions``.
        self.extra_cflags = []
        #: List of extra linker flags. Added to ``linkoptions``.
        self.extra_ldflags = []
        #: List of extra preprocessor definitions. Added to ``defines``.
        self.extra_defines = []

    def project(self, project_name):
        """
        The returned object will also have the same properties as the workspace but will only affect
        the project with the name.
        :param project_name: The name of the project inside the workspace to be updated.
        :return: ``<PremakeProject>`` object which allow to set project specific flags.
        """
        pass

    def generate(self):
        """
        Creates a ``conantoolchain.premake5.lua`` file which will properly configure build paths,
        binary paths, configuration settings and compiler/linker flags based on toolchain
        configuration.
        """
        pass

    def _target_build_os(self):
        pass
