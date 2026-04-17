"""Makefile generator for Conan dependencies

This generator creates a Makefile (conandeps.mk) with variables for each dependency and consider their components.
To simplify its usage, it also creates global variables with aggregated values from all dependencies.
This generator does not work like a toolchain, it does not include settings.

For better customization, it allows appending prefixes as flags variables:

- CONAN_LIB_FLAG: Add a prefix to all libs variables, e.g. -l
- CONAN_DEFINE_FLAG: Add a prefix to all defines variables, e.g. -D
- CONAN_SYSTEM_LIB_FLAG: Add a prefix to all system_libs variables, e.g. -l
- CONAN_INCLUDE_DIR_FLAG: Add a prefix to all include dirs variables, e.g. -I
- CONAN_LIB_DIR_FLAG: Add a prefix to all lib dirs variables, e.g. -L
- CONAN_BIN_DIR_FLAG: Add a prefix to all bin dirs variables, e.g. -L


The conandeps.mk file layout is as follows:

- CONAN_DEPS: list all transitive and direct dependencies names without version (e.g. zlib)
- Iterate over each dependency and its components:
    - Prints name, version, root folder, regular folders, libs and flags
    - Components are rootified to avoid repeating same prefix twice for the root folder
    - Components libs, folder and flags are solved as variables to avoid repeating same name twice
- Aggregated global variables for simplification, sum all dependencies to common variables (e.g. CONAN_INCLUDE_DIRS)

"""

import os
import re
import textwrap

from jinja2 import Template, StrictUndefined
from typing import Optional

from conan.api.output import ConanOutput
from conan.internal import check_duplicated_generator
from conan.tools.files import save


CONAN_MAKEFILE_FILENAME = "conandeps.mk"


def _get_formatted_dirs(folders: list, prefix_path_: str, name: str) -> list:
    """ Format the directories to be used in the makefile, adding the prefix path if needed
    :param folders: list of directories
    :param prefix_path_: prefix path
    :param name: component name
    :return: list of formatted directories
    """
    pass


def _makefy(name: str) -> str:
    """
    Convert a name to Make-variable-friendly syntax
    :param name: The name to be converted
    :return: Safe makefile variable, not including bad characters that are not parsed correctly
    """
    pass


def _makefy_properties(properties: Optional[dict]) -> dict:
    """
    Convert property dictionary keys to Make-variable-friendly syntax
    :param properties: The property dictionary to be converted (None is also accepted)
    :return: Modified property dictionary with keys not including bad characters that are not parsed correctly
    """
    pass


def _check_property_value(name, value, output):
    pass


def _filter_properties(properties: Optional[dict], output) -> dict:
    """
    Filter out properties whose values contain newlines, because they would break the generated makefile
    :param properties: A property dictionary (None is also accepted)
    :return: A property dictionary without the properties containing newlines
    """
    pass


def _conan_prefix_flag(variable: str) -> str:
    """
    Return a global flag to be used as prefix to any value in the makefile
    """
    pass


def _common_cppinfo_variables() -> dict:
    """
    Regular cppinfo variables exported by any Conanfile and their Makefile prefixes
    """
    pass


def _common_cppinfo_dirs() -> dict:
    """
    Regular cppinfo folders exported by any Conanfile and their Makefile prefixes
    """
    pass


def _jinja_format_list_values() -> str:
    """
    Template method to format a list of values in a Makefile,
    - Empty variables are not exposed in the Makefile
    - Single value variables are exposed in a single line
    - Multiple value variables are exposed in multiple lines with a tabulation
    e.g.
    define_variable_value("FOO", ["single_value"])
    output:
    FOO = single_value

    define_variable_value("BAR", ["value1", "value2"])
    output:
    BAR = \
        value1 \
        value2
    """
    pass


class MakeInfo:
    """
    Store temporary information about each dependency
    """

    def __init__(self, name: str, dirs: list, flags: list):
        """
        :param name: Dependency or component raw name
        :param dirs: cpp_info folders supported by the dependency
        :param flags: cpp_info variables supported by the dependency
        """
        self._name = name
        self._dirs = dirs
        self._flags = flags

    @property
    def name(self) -> str:
        pass

    @property
    def dirs(self) -> list:
        """
        :return: List of cpp_info folders supported by the dependency without duplicates
        """
        pass

    @property
    def flags(self) -> list:
        """
        :return: List of cpp_info variables supported by the dependency without duplicates
        """
        pass

    def dirs_append(self, directory: str):
        """
        Add a new cpp_info folder to the dependency
        """
        pass

    def flags_append(self, flag: str):
        """
        Add a new cpp_info variable to the dependency
        """
        pass


class GlobalContentGenerator:
    """
    Generates the formatted content for global variables (e.g. CONAN_DEPS, CONAN_LIBS)
    """

    template = textwrap.dedent("""\

            # Aggregated global variables

            {{ define_variable_value("CONAN_INCLUDE_DIRS", deps_cpp_info_dirs.include_dirs) -}}
            {{- define_variable_value("CONAN_LIB_DIRS", deps_cpp_info_dirs.lib_dirs) -}}
            {{- define_variable_value("CONAN_BIN_DIRS", deps_cpp_info_dirs.bin_dirs) -}}
            {{- define_variable_value("CONAN_SRC_DIRS", deps_cpp_info_dirs.src_dirs) -}}
            {{- define_variable_value("CONAN_BUILD_DIRS", deps_cpp_info_dirs.build_dirs) -}}
            {{- define_variable_value("CONAN_RES_DIRS", deps_cpp_info_dirs.res_dirs) -}}
            {{- define_variable_value("CONAN_FRAMEWORK_DIRS", deps_cpp_info_dirs.framework_dirs) -}}
            {{- define_variable_value("CONAN_OBJECTS", deps_cpp_info_flags.objects) -}}
            {{- define_variable_value("CONAN_LIBS", deps_cpp_info_flags.libs) -}}
            {{- define_variable_value("CONAN_DEFINES", deps_cpp_info_flags.defines) -}}
            {{- define_variable_value("CONAN_CFLAGS", deps_cpp_info_flags.cflags) -}}
            {{- define_variable_value("CONAN_CXXFLAGS", deps_cpp_info_flags.cxxflags) -}}
            {{- define_variable_value("CONAN_SHAREDLINKFLAGS", deps_cpp_info_flags.sharedlinkflags) -}}
            {{- define_variable_value("CONAN_EXELINKFLAGS", deps_cpp_info_flags.exelinkflags) -}}
            {{- define_variable_value("CONAN_FRAMEWORKS", deps_cpp_info_flags.frameworks) -}}
            {{- define_variable_value("CONAN_REQUIRES", deps_cpp_info_flags.requires) -}}
            {{- define_variable_value("CONAN_SYSTEM_LIBS", deps_cpp_info_flags.system_libs) -}}
            """)

    template_deps = textwrap.dedent("""\
            {{ define_variable_value("CONAN_DEPS", deps) }}
            """)

    def content(self, deps_cpp_info_dirs: dict, deps_cpp_info_flags: dict) -> str:
        """
        Generate content for Cppinfo variables (e.g. CONAN_LIBS, CONAN_INCLUDE_DIRS)
        :param deps_cpp_info_dirs: Formatted dependencies folders
        :param deps_cpp_info_flags: Formatted dependencies variables
        """
        pass

    def deps_content(self, dependencies_names: list) -> str:
        """
        Generate content for CONAN_DEPS (e.g. CONAN_DEPS = zlib, openssl)
        :param dependencies_names: Non-formatted dependencies names
        """
        pass


class GlobalGenerator:
    """
    Process all collected dependencies and parse to generate global content
    """

    def __init__(self, conanfile, make_infos):
        self._conanfile = conanfile
        self._make_infos = make_infos

    def _get_dependency_dirs(self) -> dict:
        """
        List regular directories from cpp_info and format them to be used in the makefile
        """
        pass

    def _get_dependency_flags(self) -> dict:
        """
        List common variables from cpp_info and format them to be used in the makefile
        """
        pass

    def generate(self) -> str:
        """
        Process folder and variables for a dependency and generates its Makefile content
        """
        pass

    def deps_generate(self) -> str:
        """
        Process dependencies names and generates its Makefile content.
        It should be added as first variable in the Makefile.
        """
        pass


class DepComponentContentGenerator:
    """
    Generates Makefile content for each dependency component
    """

    template = textwrap.dedent("""\
        # {{ dep.ref.name }}::{{ comp_name }}

        {{  define_variable_value_safe("CONAN_INCLUDE_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'include_dirs') -}}
        {{- define_variable_value_safe("CONAN_LIB_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'lib_dirs') -}}
        {{- define_variable_value_safe("CONAN_BIN_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'bin_dirs') -}}
        {{- define_variable_value_safe("CONAN_SRC_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'src_dirs') -}}
        {{- define_variable_value_safe("CONAN_BUILD_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'build_dirs') -}}
        {{- define_variable_value_safe("CONAN_RES_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'res_dirs') -}}
        {{- define_variable_value_safe("CONAN_FRAMEWORK_DIRS_{}_{}".format(dep_name, name), cpp_info_dirs, 'framework_dirs') -}}
        {{- define_variable_value_safe("CONAN_OBJECTS_{}_{}".format(dep_name, name), cpp_info_flags, 'objects') -}}
        {{- define_variable_value_safe("CONAN_LIBS_{}_{}".format(dep_name, name), cpp_info_flags, 'libs') -}}
        {{- define_variable_value_safe("CONAN_DEFINES_{}_{}".format(dep_name, name), cpp_info_flags, 'defines') -}}
        {{- define_variable_value_safe("CONAN_CFLAGS_{}_{}".format(dep_name, name), cpp_info_flags, 'cflags') -}}
        {{- define_variable_value_safe("CONAN_CXXFLAGS_{}_{}".format(dep_name, name), cpp_info_flags, 'cxxflags') -}}
        {{- define_variable_value_safe("CONAN_SHAREDLINKFLAGS_{}_{}".format(dep_name, name), cpp_info_flags, 'sharedlinkflags') -}}
        {{- define_variable_value_safe("CONAN_EXELINKFLAGS_{}_{}".format(dep_name, name), cpp_info_flags, 'exelinkflags') -}}
        {{- define_variable_value_safe("CONAN_FRAMEWORKS_{}_{}".format(dep_name, name), cpp_info_flags, 'frameworks') -}}
        {{- define_variable_value_safe("CONAN_REQUIRES_{}_{}".format(dep_name, name), cpp_info_flags, 'requires') -}}
        {{- define_variable_value_safe("CONAN_SYSTEM_LIBS_{}_{}".format(dep_name, name), cpp_info_flags, 'system_libs') -}}
        {{- define_multiple_variable_value("CONAN_PROPERTY_{}_{}".format(dep_name, name), properties) -}}
        """)

    def __init__(self, dependency, component_name: str, dirs: dict, flags: dict, output):
        """
        :param dependency: The dependency object that owns the component
        :param component_name: component raw name e.g. poco::poco_json
        :param dirs: The component cpp_info folders
        :param flags: The component cpp_info variables
        """
        self._dep = dependency
        self._name = component_name
        self._dirs = dirs or {}
        self._flags = flags or {}
        self._output = output

    def content(self) -> str:
        """
        Format template and generate Makefile component
        """
        pass


class DepContentGenerator:
    """
    Generates Makefile content for a dependency
    """

    template = textwrap.dedent("""\

        # {{ dep.ref }}{% if not req.direct %} (indirect dependency){% endif +%}

        CONAN_NAME_{{ name }} = {{ dep.ref.name }}
        CONAN_VERSION_{{ name }} = {{ dep.ref.version }}
        CONAN_REFERENCE_{{ name }} = {{ dep.ref }}

        CONAN_ROOT_{{ name }} = {{ root }}

        {{  define_variable_value("CONAN_SYSROOT_{}".format(name), sysroot) -}}
        {{- define_variable_value_safe("CONAN_INCLUDE_DIRS_{}".format(name), cpp_info_dirs, 'include_dirs') -}}
        {{- define_variable_value_safe("CONAN_LIB_DIRS_{}".format(name), cpp_info_dirs, 'lib_dirs') -}}
        {{- define_variable_value_safe("CONAN_BIN_DIRS_{}".format(name), cpp_info_dirs, 'bin_dirs') -}}
        {{- define_variable_value_safe("CONAN_SRC_DIRS_{}".format(name), cpp_info_dirs, 'src_dirs') -}}
        {{- define_variable_value_safe("CONAN_BUILD_DIRS_{}".format(name), cpp_info_dirs, 'build_dirs') -}}
        {{- define_variable_value_safe("CONAN_RES_DIRS_{}".format(name), cpp_info_dirs, 'res_dirs') -}}
        {{- define_variable_value_safe("CONAN_FRAMEWORK_DIRS_{}".format(name), cpp_info_dirs, 'framework_dirs') -}}
        {{- define_variable_value_safe("CONAN_OBJECTS_{}".format(name), cpp_info_flags, 'objects') -}}
        {{- define_variable_value_safe("CONAN_LIBS_{}".format(name), cpp_info_flags, 'libs') -}}
        {{- define_variable_value_safe("CONAN_DEFINES_{}".format(name), cpp_info_flags, 'defines') -}}
        {{- define_variable_value_safe("CONAN_CFLAGS_{}".format(name), cpp_info_flags, 'cflags') -}}
        {{- define_variable_value_safe("CONAN_CXXFLAGS_{}".format(name), cpp_info_flags, 'cxxflags') -}}
        {{- define_variable_value_safe("CONAN_SHAREDLINKFLAGS_{}".format(name), cpp_info_flags, 'sharedlinkflags') -}}
        {{- define_variable_value_safe("CONAN_EXELINKFLAGS_{}".format(name), cpp_info_flags, 'exelinkflags') -}}
        {{- define_variable_value_safe("CONAN_FRAMEWORKS_{}".format(name), cpp_info_flags, 'frameworks') -}}
        {{- define_variable_value_safe("CONAN_REQUIRES_{}".format(name), cpp_info_flags, 'requires') -}}
        {{- define_variable_value_safe("CONAN_SYSTEM_LIBS_{}".format(name), cpp_info_flags, 'system_libs') -}}
        {{- define_variable_value("CONAN_COMPONENTS_{}".format(name), components) -}}
        {{- define_multiple_variable_value("CONAN_PROPERTY_{}".format(name), properties) -}}
        """)

    def __init__(self, dependency, require, root: str, sysroot, dirs: dict, flags: dict, output):
        self._dep = dependency
        self._req = require
        self._root = root
        self._sysroot = sysroot
        self._dirs = dirs or {}
        self._flags = flags or {}
        self._output = output

    def content(self) -> str:
        """
        Parse dependency variables and generate its Makefile content
        """
        pass


class DepComponentGenerator:
    """
    Generates Makefile content for a dependency component
    """

    def __init__(self, dependency, makeinfo: MakeInfo, component_name: str, component, root: str, output):
        """
        :param dependency: The dependency object that owns the component
        :param makeinfo: Makeinfo to store component variables
        :param component_name: The component raw name e.g. poco::poco_json
        :param component: The component object to obtain cpp_info variables
        :param root: The dependency root folder
        """
        self._dep = dependency
        self._name = component_name
        self._comp = component
        self._root = root
        self._makeinfo = makeinfo
        self._output = output

    def _get_component_dirs(self) -> dict:
        """
        List regular directories from cpp_info and format them to be used in the makefile
        :return: A dictionary with regular folder name and its formatted path
        """
        pass

    @staticmethod
    def _rootify(root: str, root_id: str, path_list: list) -> list:
        """
        Replaces component folder path by its root node folder path in case they match
        :param root: root folder path for component's father
        :param root_id: component's dependency name
        :param path_list: folder list available in the component
        :return: A formatted folder list, solving root folder path as prefix
        """
        pass

    def _get_component_flags(self) -> dict:
        """
        List common variables from cpp_info and format them to be used in the makefile
        :return: A dictionary with regular flag/variable name and its formatted value with prefix
        """
        pass

    def generate(self) -> str:
        """
        Process component cpp_info variables and generate its Makefile content
        :return: Component Makefile content
        """
        pass


class DepGenerator:
    """
    Process a dependency cpp_info variables and generate its Makefile content
    """

    def __init__(self, dependency, require, output):
        self._dep = dependency
        self._req = require
        self._info = MakeInfo(self._dep.ref.name, [], [])
        self._output = output

    @property
    def makeinfo(self) -> MakeInfo:
        """
        :return: Dependency folder and flags
        """
        pass

    def _get_dependency_dirs(self, root: str, dependency) -> dict:
        """
        List regular directories from cpp_info and format them to be used in the makefile
        :param root: Package root folder
        :param dependency: Dependency object
        :return: A dictionary with regular folder name and its formatted path
        """
        pass

    def _get_dependency_flags(self, dependency) -> dict:
        """
        List common variables from cpp_info and format them to be used in the makefile
        :param dependency: Dependency object
        """
        pass

    def _get_sysroot(self, root: str) -> list:
        """
        Get the sysroot of the dependency. Sysroot is a list of directories, or a single directory
        """
        pass

    def _get_root_folder(self):
        """
        Get the root folder of the dependency
        """
        pass

    def generate(self) -> str:
        """
        Process dependency folders and flags to generate its Makefile content. Plus, execute same
        steps for each component
        """
        pass


class MakeDeps:
    """
    Generates a Makefile with the variables needed to build a project with the specified.
    """

    _title = "# This Makefile has been generated by Conan. DO NOT EDIT!\n"

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile

    def generate(self) -> None:
        """
        Collects all dependencies and components, then, generating a Makefile
        """
        pass
