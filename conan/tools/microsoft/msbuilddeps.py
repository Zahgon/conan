import fnmatch
import os
import re
import textwrap
from xml.dom import minidom

from jinja2 import Template

from conan.internal import check_duplicated_generator
from conan.errors import ConanException
from conan.internal.api.install.generators import relativize_path
from conan.internal.model.dependencies import get_transitive_requires
from conan.tools.microsoft.visual import msvc_platform_from_arch
from conan.internal.util.files import load, save

VALID_LIB_EXTENSIONS = (".so", ".lib", ".a", ".dylib", ".bc")


class MSBuildDeps:
    """
    MSBuildDeps class generator
    conandeps.props: unconditional import of all *direct* dependencies only
    """

    _vars_props = textwrap.dedent("""\
        <?xml version="1.0" encoding="utf-8"?>
        <Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
          <PropertyGroup Label="ConanVariables">
            <Conan{{name}}RootFolder>{{root_folder}}</Conan{{name}}RootFolder>
            <Conan{{name}}BinaryDirectories>{{bin_dirs}}</Conan{{name}}BinaryDirectories>
            {% if host_context %}
            <Conan{{name}}CompilerFlags>{{compiler_flags}}</Conan{{name}}CompilerFlags>
            <Conan{{name}}LinkerFlags>{{linker_flags}}</Conan{{name}}LinkerFlags>
            <Conan{{name}}PreprocessorDefinitions>{{definitions}}</Conan{{name}}PreprocessorDefinitions>
            <Conan{{name}}IncludeDirectories>{{include_dirs}}</Conan{{name}}IncludeDirectories>
            <Conan{{name}}ResourceDirectories>{{res_dirs}}</Conan{{name}}ResourceDirectories>
            <Conan{{name}}LibraryDirectories>{{lib_dirs}}</Conan{{name}}LibraryDirectories>
            <Conan{{name}}Libraries>{{libs}}</Conan{{name}}Libraries>
            <Conan{{name}}SystemLibs>{{system_libs}}</Conan{{name}}SystemLibs>
            {% endif %}
          </PropertyGroup>
        </Project>
        """)

    _conf_props = textwrap.dedent("""\
        <?xml version="1.0" encoding="utf-8"?>
        <Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
          <ImportGroup Label="PropertySheets">
            {% for dep in deps %}
            <Import Condition="'$(conan_{{dep}}_props_imported)' != 'True'" Project="conan_{{dep}}.props"/>
            {% endfor %}
          </ImportGroup>
          <ImportGroup Label="PropertySheets">
            <Import Project="{{vars_filename}}"/>
          </ImportGroup>
          {% if host_context %}
          <PropertyGroup>
            <ConanDebugPath>$(Conan{{name}}BinaryDirectories);$(ConanDebugPath)</ConanDebugPath>
            <LocalDebuggerEnvironment>PATH=$(ConanDebugPath);%PATH%</LocalDebuggerEnvironment>
            <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
            {% if ca_exclude %}
            <CAExcludePath>$(Conan{{name}}IncludeDirectories);$(CAExcludePath)</CAExcludePath>
            {% endif %}
          </PropertyGroup>
          <ItemDefinitionGroup>
            <ClCompile>
              <AdditionalIncludeDirectories>$(Conan{{name}}IncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
              <PreprocessorDefinitions>$(Conan{{name}}PreprocessorDefinitions)%(PreprocessorDefinitions)</PreprocessorDefinitions>
              <AdditionalOptions>$(Conan{{name}}CompilerFlags) %(AdditionalOptions)</AdditionalOptions>
            </ClCompile>
            <Link>
              <AdditionalLibraryDirectories>$(Conan{{name}}LibraryDirectories)%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
              <AdditionalDependencies>$(Conan{{name}}Libraries)%(AdditionalDependencies)</AdditionalDependencies>
              <AdditionalDependencies>$(Conan{{name}}SystemLibs)%(AdditionalDependencies)</AdditionalDependencies>
              <AdditionalOptions>$(Conan{{name}}LinkerFlags) %(AdditionalOptions)</AdditionalOptions>
            </Link>
            <Midl>
              <AdditionalIncludeDirectories>$(Conan{{name}}IncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
            </Midl>
            <ResourceCompile>
              <AdditionalIncludeDirectories>$(Conan{{name}}IncludeDirectories)%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
              <PreprocessorDefinitions>$(Conan{{name}}PreprocessorDefinitions)%(PreprocessorDefinitions)</PreprocessorDefinitions>
            </ResourceCompile>
          </ItemDefinitionGroup>
          {% else %}
          <PropertyGroup>
            <ExecutablePath>$(Conan{{name}}BinaryDirectories)$(ExecutablePath)</ExecutablePath>
          </PropertyGroup>
          {% endif %}
        </Project>
        """)

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        #: Defines the build type. By default, the value of ``settings.build_type``.
        self.configuration = conanfile.settings.build_type
        #: Defines the configuration key used to conditionally select which property sheet to
        #: import (defaults to ``"Configuration"``).
        self.configuration_key = "Configuration"
        # TODO: This platform is not exactly the same as ``msbuild_arch``, because it differs
        # in x86=>Win32
        #: Platform name, e.g., ``Win32`` if ``settings.arch == "x86"``.
        self.platform = msvc_platform_from_arch(str(conanfile.settings.arch))
        #: Defines the platform key used to conditionally select which property sheet to
        #: import (defaults to ``"Platform"``).
        self.platform_key = "Platform"
        ca_exclude = "tools.microsoft.msbuilddeps:exclude_code_analysis"
        #: List of packages names patterns to add Visual Studio ``CAExcludePath`` property
        #: to each match as part of its ``conan_[DEP]_[CONFIG].props``. By default, value given by
        #: ``tools.microsoft.msbuilddeps:exclude_code_analysis`` configuration.
        self.exclude_code_analysis = self._conanfile.conf.get(ca_exclude, check_type=list)

    def generate(self):
        """
        Generates ``conan_<pkg>_<config>_vars.props``, ``conan_<pkg>_<config>.props``,
        and ``conan_<pkg>.props`` files into the ``conanfile.generators_folder``.
        """
        pass

    def _config_filename(self):
        pass

    def _condition(self):
        pass

    @staticmethod
    def _dep_name(dep, build):
        pass

    @staticmethod
    def _get_valid_xml_format(name):
        pass

    def _vars_props_file(self, require, dep, name, cpp_info, build):
        """
        content for conan_vars_poco_x86_release.props, containing the variables for 1 config
        This will be for 1 package or for one component of a package
        :return: varfile content
        """
        pass

    def _activate_props_file(self, dep_name, vars_filename, deps, build):
        """
        Actual activation of the VS variables, per configuration
            - conan_pkgname_x86_release.props / conan_pkgname_compname_x86_release.props
        :param dep_name: pkgname / pkgname_compname
        :param deps: the name of other things to be included: [dep1, dep2:compA, ...]
        :param build: if it is a build require or not
        """
        pass

    @staticmethod
    def _dep_props_file(dep_name, filename, aggregated_filename, condition, content=None):
        """
        The file aggregating all configurations for a given pkg / component
            - conan_pkgname.props
        """
        pass

    def _conandeps(self):
        """ this is a .props file including direct declared dependencies
        """
        pass

    def _package_props_files(self, require, dep, build=False):
        """ all the files for a given package:
        - conan_pkgname_vars_config.props: definition of variables, one per config
        - conan_pkgname_config.props: The one using those variables. This is very different for
                                      Host and build, build only activate <ExecutablePath>
        - conan_pkgname.props: Conditional aggregate xxx_config.props based on active config
        """
        pass

    def _content(self):
        pass
