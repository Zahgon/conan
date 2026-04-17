import os
import re
import textwrap

from jinja2 import Template

from conan.internal import check_duplicated_generator
from conan.errors import ConanException
from conan.internal.model.dependencies import get_transitive_requires
from conan.internal.util.files import load, save
from conan.tools.apple.apple import _to_apple_arch

GLOBAL_XCCONFIG_TEMPLATE = textwrap.dedent("""\
    // Includes both the toolchain and the dependencies
    // files if they exist

    """)

GLOBAL_XCCONFIG_FILENAME = "conan_config.xcconfig"


def _format_name(name):
    pass


def _xcconfig_settings_filename(settings, configuration):
    pass


def _xcconfig_conditional(settings, configuration):
    pass


def _add_includes_to_file_or_create(filename, template, files_to_include):
    pass


class XcodeDeps:
    general_name = "conandeps.xcconfig"

    _conf_xconfig = textwrap.dedent("""\
        PACKAGE_ROOT_{{pkg_name}}{{condition}} = {{root}}
        // Compiler options for {{pkg_name}}::{{comp_name}}
        SYSTEM_HEADER_SEARCH_PATHS_{{pkg_name}}_{{comp_name}}{{condition}} = {{include_dirs}}
        GCC_PREPROCESSOR_DEFINITIONS_{{pkg_name}}_{{comp_name}}{{condition}} = {{definitions}}
        OTHER_CFLAGS_{{pkg_name}}_{{comp_name}}{{condition}} = {{c_compiler_flags}}
        OTHER_CPLUSPLUSFLAGS_{{pkg_name}}_{{comp_name}}{{condition}} = {{cxx_compiler_flags}}
        FRAMEWORK_SEARCH_PATHS_{{pkg_name}}_{{comp_name}}{{condition}} = {{frameworkdirs}}

        // Link options for {{pkg_name}}::{{comp_name}}
        LIBRARY_SEARCH_PATHS_{{pkg_name}}_{{comp_name}}{{condition}} = {{lib_dirs}}
        OTHER_LDFLAGS_{{pkg_name}}_{{comp_name}}{{condition}} = {{linker_flags}} {{libs}} {{system_libs}} {{frameworks}}
        """)

    _dep_xconfig = textwrap.dedent("""\
        // Conan XcodeDeps generated file for {{pkg_name}}::{{comp_name}}
        // Includes all configurations for each dependency
        {% for include in deps_includes %}
        #include "{{include}}"
        {% endfor %}
        #include "{{dep_xconfig_filename}}"

        SYSTEM_HEADER_SEARCH_PATHS = $(inherited) $(SYSTEM_HEADER_SEARCH_PATHS_{{pkg_name}}_{{comp_name}})
        GCC_PREPROCESSOR_DEFINITIONS = $(inherited) $(GCC_PREPROCESSOR_DEFINITIONS_{{pkg_name}}_{{comp_name}})
        OTHER_CFLAGS = $(inherited) $(OTHER_CFLAGS_{{pkg_name}}_{{comp_name}})
        OTHER_CPLUSPLUSFLAGS = $(inherited) $(OTHER_CPLUSPLUSFLAGS_{{pkg_name}}_{{comp_name}})
        FRAMEWORK_SEARCH_PATHS = $(inherited) $(FRAMEWORK_SEARCH_PATHS_{{pkg_name}}_{{comp_name}})

        // Link options for {{pkg_name}}_{{comp_name}}
        LIBRARY_SEARCH_PATHS = $(inherited) $(LIBRARY_SEARCH_PATHS_{{pkg_name}}_{{comp_name}})
        OTHER_LDFLAGS = $(inherited) $(OTHER_LDFLAGS_{{pkg_name}}_{{comp_name}})
        """)

    _all_xconfig = textwrap.dedent("""\
        // Conan XcodeDeps generated file
        // Includes all direct dependencies
        """)

    _pkg_xconfig = textwrap.dedent("""\
        // Conan XcodeDeps generated file
        // Includes all components for the package
        """)

    def __init__(self, conanfile):
        self._conanfile = conanfile
        self.configuration = conanfile.settings.get_safe("build_type")
        arch = conanfile.settings.get_safe("arch")
        self.architecture = _to_apple_arch(arch, default=arch)
        self.os_version = conanfile.settings.get_safe("os.version")
        self.sdk = conanfile.settings.get_safe("os.sdk")
        self.sdk_version = conanfile.settings.get_safe("os.sdk_version")

    def generate(self):
        pass

    def _conf_xconfig_file(self, require, pkg_name, comp_name, package_folder, transitive_cpp_infos):
        """
        content for conan_poco_x86_release.xcconfig, containing the activation
        """
        pass

    def _dep_xconfig_file(self, pkg_name, comp_name, name_general, dep_xconfig_filename, reqs):
        # Current directory is the generators_folder
        pass

    def _all_xconfig_file(self, deps, content):
        """
        this is a .xcconfig file including all declared dependencies
        """
        pass

    def _pkg_xconfig_file(self, components):
        """
        this is a .xcconfig file including the components for each package
        """
        pass

    @property
    def _global_xconfig_content(self):
        pass

    def get_content_for_component(self, require, pkg_name, component_name, package_folder, transitive_internal, transitive_external):
        pass

    def _content(self):
        pass
