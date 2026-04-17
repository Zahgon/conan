import os
import re
import textwrap

from jinja2 import Template, StrictUndefined

from conan.errors import ConanException
from conan.internal import check_duplicated_generator
from conan.internal.model.dependencies import get_transitive_requires
from conan.internal.util.files import save


class _PCFilesDeps:

    template = textwrap.dedent("""\
        {% for k, v in pc_variables.items() %}
        {{ "{}={}".format(k, v) }}
        {% endfor %}

        Name: {{ name }}
        Description: {{ description }}
        Version: {{ version }}
        {% if libflags %}
        Libs: {{ libflags }}
        {% endif %}
        {% if cflags %}
        Cflags: {{ cflags }}
        {% endif %}
        {% if requires|length %}
        Requires: {{ requires|join(' ') }}
        {% endif %}
    """)

    alias_template = textwrap.dedent("""\
        Name: {{name}}
        Description: Alias {{name}} for {{aliased}}
        Version: {{version}}
        Requires: {{aliased}}
    """)

    def __init__(self, pkgconfigdeps, dep, suffix=""):
        self._conanfile = pkgconfigdeps._conanfile  # noqa
        self._properties = pkgconfigdeps._properties  # noqa
        self._transitive_reqs = get_transitive_requires(self._conanfile, dep)
        self._dep = dep
        self._suffix = suffix

    def _get_aliases(self, dep, pkg_name=None, comp_ref_name=None):
        pass

    def _get_name(self, dep, pkg_name=None, comp_ref_name=None):
        pass

    def _get_property(self, prop, dep, comp_name=None, check_type=None):
        pass

    def _get_pc_variables(self, dep, cpp_info, custom_content=None):
        """
        Get all the freeform variables defined by Conan and
        users (through ``pkg_config_custom_content``). This last ones will override the
        Conan defined variables.
        """
        pass

    @staticmethod
    def _get_formatted_dirs(folder_name, folders, prefix_path_):
        pass

    def _get_framework_flags(self, cpp_info):
        # FIXME: GnuDepsFlags used only here. Let's adapt the code and remove this dependency.
        #        self._conanfile is also used only here.
        pass

    def _get_lib_flags(self, libdirvars, cpp_info):
        pass

    def _get_cflags(self, includedirvars, cpp_info):
        pass

    def _get_component_requirement_names(self, cpp_info):
        """
        Get all the pkg-config valid names from the requirements ones given a CppInfo object.

        For instance, those requirements could be coming from:

        ```python
        from conan import ConanFile
        class PkgConfigConan(ConanFile):
            requires = "other/1.0"

            def package_info(self):
                self.cpp_info.requires = ["other::cmp1"]

            # Or:

            def package_info(self):
                self.cpp_info.components["cmp"].requires = ["other::cmp1"]
        ```
        """
        pass

    def items(self):
        """
        Get all the PC files and contents for any dependency:

        * If the given dependency does not have components:
            The PC file will be the dependency one.

        * If the given dependency has components:
            The PC files will be saved in this order:
                1- Package components.
                2- Root component.

            Note: If the root-package PC name matches with any other of the components one, the first one
            is not going to be created. Components have more priority than root package.

        * Apart from those PC files, if there are any aliases declared, they will be created too.
        """
        pc_files = {}
        pc_alias_files = {}
        pkg_name = self._get_name(self._dep)
        # First, let's load all the components PC files
        # Loop through all the package's components
        for comp_ref_name, comp_cpp_info in self._dep.cpp_info.get_sorted_components().items():
            # At first, let's check if we have defined some components requires, e.g., "dep::cmp1"
            comp_requires = self._get_component_requirement_names(comp_cpp_info)
            comp_name = self._get_name(self._dep, pkg_name, comp_ref_name)
            version = (self._get_property("component_version", self._dep, comp_ref_name) or
                       self._get_property("system_package_version", self._dep, comp_ref_name) or
                       self._dep.ref.version)
            custom_content = self._get_property("pkg_config_custom_content", self._dep, comp_ref_name)
            pc_variables = self._get_pc_variables(self._dep, comp_cpp_info, custom_content)
            pc_context = {
                "name": comp_name,
                "description": f"Conan component: {comp_name}",
                "version": version,
                "requires": comp_requires,
                "pc_variables": pc_variables,
                "cflags": self._get_cflags([d for d in pc_variables if d.startswith("includedir")],
                                           comp_cpp_info),
                "libflags": self._get_lib_flags([d for d in pc_variables if d.startswith("libdir")],
                                                comp_cpp_info)
            }
            pc_files[comp_name] = self._get_pc_content(pc_context)
            # Aliases
            for alias in self._get_aliases(self._dep, pkg_name, comp_ref_name):
                pc_alias_files[alias] = self._get_alias_pc_content({
                    "name": alias,
                    "version": version,
                    "aliased": comp_name
                })
        # Second, let's load the root package's PC file ONLY
        # if it does not already exist in components one
        # Issue related: https://github.com/conan-io/conan/issues/10341
        should_skip_main = self._get_property("pkg_config_name", self._dep) == "none"
        if pkg_name not in pc_files and not should_skip_main:
            cpp_info = self._dep.cpp_info
            # At first, let's check if we have defined some global requires, e.g., "other::cmp1"
            # Note: If DEP has components, they'll be the requirements == pc_files.keys()
            requires = list(pc_files.keys()) or self._get_component_requirement_names(cpp_info)
            # If we have found some component requirements it would be enough
            if not requires:
                # If no requires were found, let's try to get all the direct visible dependencies,
                # e.g., requires = "other_pkg/1.0"
                requires = [self._get_name(req) for req in self._transitive_reqs.values()]
            version = (self._get_property("system_package_version", self._dep)
                       or self._dep.ref.version)
            custom_content = self._get_property("pkg_config_custom_content", self._dep)
            pc_variables = self._get_pc_variables(self._dep, cpp_info, custom_content)
            pc_context = {
                "name": pkg_name,
                "description": f"Conan package: {pkg_name}",
                "version": version,
                "requires": requires,
                "pc_variables": pc_variables,
                "cflags": self._get_cflags([d for d in pc_variables if d.startswith("includedir")],
                                           cpp_info),
                "libflags": self._get_lib_flags([d for d in pc_variables if d.startswith("libdir")],
                                                cpp_info)
            }
            pc_files[pkg_name] = self._get_pc_content(pc_context)
            # Aliases
            for alias in self._get_aliases(self._dep):
                pc_alias_files[alias] = self._get_alias_pc_content({
                    "name": alias,
                    "version": version,
                    "aliased": pkg_name
                })
        # Adding the aliases
        pc_files.update(pc_alias_files)
        return pc_files.items()

    def _get_pc_content(self, context):
        pass

    def _get_alias_pc_content(self, context):
        pass


class PkgConfigDeps:

    def __init__(self, conanfile):
        self._conanfile = conanfile
        # Activate the build *.pc files for the specified libraries
        self.build_context_activated = []
        # If specified, the files/requires/names for the build context will be renamed appending
        # a suffix. It is necessary in case of same require and build_require and will cause an error
        # DEPRECATED: consumers should use build_context_folder instead
        # FIXME: Conan 3.x: Remove build_context_suffix attribute
        self.build_context_suffix = {}
        # By default, the "[generators_folder]/build" folder will save all the *.pc files activated
        # in the build_context_activated list.
        # Notice that if the `build_context_suffix` attr is defined, the `build_context_folder` one
        # will have no effect.
        # Issue: https://github.com/conan-io/conan/issues/12342
        # Issue: https://github.com/conan-io/conan/issues/14935
        # FIXME: Conan 3.x: build_context_folder should be "build" by default
        self.build_context_folder = None  # Keeping backward-compatibility
        self._properties = {}

    def _get_dependencies(self):
        # Get all the dependencies
        pass

    def generate(self):
        """
        Save all the `*.pc` files
        """
        pass

    def set_property(self, dep, prop, value):
        """
        Using this method you can overwrite the :ref:`property<PkgConfigDeps Properties>` values set by
        the Conan recipes from the consumer. This can be done for `pkg_config_name`,
        `pkg_config_aliases` and `pkg_config_custom_content` properties.

        :param dep: Name of the dependency to set the :ref:`property<PkgConfigDeps Properties>`. For
         components use the syntax: ``dep_name::component_name``.
        :param prop: Name of the :ref:`property<PkgConfigDeps Properties>`.
        :param value: Value of the property. Use ``None`` to invalidate any value set by the
         upstream recipe.
        """
        pass
