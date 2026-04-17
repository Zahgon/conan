import os
import textwrap
from xml.dom import minidom

from jinja2 import Template

from conan.internal import check_duplicated_generator
from conan.internal.api.detect.detect_vs import vs_installation_path
from conan.tools.build import build_jobs
from conan.tools.intel.intel_cc import IntelCC
from conan.tools.microsoft.visual import VCVars, msvs_toolset, msvc_runtime_flag, \
    msvc_platform_from_arch, vs_ide_version
from conan.errors import ConanException
from conan.internal.util.files import save, load


class MSBuildToolchain:
    """
    MSBuildToolchain class generator
    """

    filename = "conantoolchain.props"

    _config_toolchain_props = textwrap.dedent("""\
        <?xml version="1.0" encoding="utf-8"?>
        <Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
          {% if toolset_version_full_path %}
          <Import Project="{{toolset_version_full_path}}" />
          {% endif %}
          <ItemDefinitionGroup>
            <ClCompile>
              <PreprocessorDefinitions>{{ defines }}%(PreprocessorDefinitions)</PreprocessorDefinitions>
              <AdditionalOptions>{{ compiler_flags }} %(AdditionalOptions)</AdditionalOptions>
              <RuntimeLibrary>{{ runtime_library }}</RuntimeLibrary>
              {% if cstd %}<LanguageStandard_C>{{ cstd }}</LanguageStandard_C>{% endif %}
              <LanguageStandard>{{ cppstd }}</LanguageStandard>{{ parallel }}{{ compile_options }}
            </ClCompile>
            <Link>
              <AdditionalOptions>{{ linker_flags }} %(AdditionalOptions)</AdditionalOptions>
            </Link>
            <ResourceCompile>
              <PreprocessorDefinitions>{{ defines }}%(PreprocessorDefinitions)</PreprocessorDefinitions>
              {% if rc_flags %}<AdditionalOptions>{{ rc_flags }} %(AdditionalOptions)</AdditionalOptions>{% endif %}
            </ResourceCompile>
          </ItemDefinitionGroup>
          <PropertyGroup Label="Configuration">
            {% if winsdk_version %}
            <WindowsTargetPlatformVersion>{{ winsdk_version}}</WindowsTargetPlatformVersion>
            {% endif %}
            <PlatformToolset>{{ toolset }}</PlatformToolset>
            {% for k, v in properties.items() %}
            <{{k}}>{{ v }}</{{k}}>
            {% endfor %}
          </PropertyGroup>
        </Project>
    """)

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        #: Dict-like that defines the preprocessor definitions
        self.preprocessor_definitions = {}
        #: Dict with compile options that will be added as <key>value</key> in the ClCompile section
        self.compile_options = {}
        #: List of all the CXX flags
        self.cxxflags = []
        #: List of all the C flags
        self.cflags = []
        #: List of all the LD linker flags
        self.ldflags = []
        #: List of all the RC (resource compiler) flags
        self.rcflags = []
        #: The build type. By default, the ``conanfile.settings.build_type`` value
        self.configuration = conanfile.settings.build_type
        #: The runtime flag. By default, it'll be based on the `compiler.runtime` setting.
        self.runtime_library = self._runtime_library()
        #: cppstd value. By default, ``compiler.cppstd`` one.
        self.cppstd = conanfile.settings.get_safe("compiler.cppstd")
        self.cstd = conanfile.settings.get_safe("compiler.cstd")
        #: VS IDE Toolset, e.g., ``"v140"``. If ``compiler=msvc``, you can use ``compiler.toolset``
        #: setting, else, it'll be based on ``msvc`` version.
        self.toolset = msvs_toolset(conanfile)
        self.properties = {}
        self.toolset_version_full_path = _get_toolset_props(conanfile)

    def _name_condition(self, settings):
        pass

    def generate(self):
        """
        Generates a ``conantoolchain.props``, a ``conantoolchain_<config>.props``, and,
        if ``compiler=msvc``, a ``conanvcvars.bat`` files. In the first two cases, they'll have the
        valid XML format with all the good settings like any other VS project ``*.props`` file. The
        last one emulates the ``vcvarsall.bat`` env script. See also :class:`VCVars`.
        """
        pass

    def _runtime_library(self):
        pass

    @property
    def context_config_toolchain(self):

        pass

    def _write_config_toolchain(self, config_filename):
        pass

    def _write_main_toolchain(self, config_filename, condition):
        pass

    def _get_extra_flags(self):
        # Now, it's time to get all the flags defined by the user
        pass


def _get_toolset_props(conanfile):
    pass
