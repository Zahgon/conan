import textwrap

import jinja2
from jinja2 import Template

from conan.api.output import Color
from conan.internal import check_duplicated_generator
from conan.tools.cmake.cmakedeps import FIND_MODE_CONFIG, FIND_MODE_NONE, FIND_MODE_BOTH, \
    FIND_MODE_MODULE
from conan.tools.cmake.cmakedeps.templates.config import ConfigTemplate
from conan.tools.cmake.cmakedeps.templates.config_version import ConfigVersionTemplate
from conan.tools.cmake.cmakedeps.templates.macros import MacrosTemplate
from conan.tools.cmake.cmakedeps.templates.target_configuration import TargetConfigurationTemplate
from conan.tools.cmake.cmakedeps.templates.target_data import ConfigDataTemplate
from conan.tools.cmake.cmakedeps.templates.targets import TargetsTemplate
from conan.tools.files import save
from conan.errors import ConanException
from conan.internal.model.dependencies import get_transitive_requires


class CMakeDeps:

    def __init__(self, conanfile):
        self._conanfile = conanfile
        self.arch = self._conanfile.settings.get_safe("arch")
        self.configuration = str(self._conanfile.settings.build_type)

        # Activate the build config files for the specified libraries
        self.build_context_activated = []
        # By default, the build modules are generated for host context only
        self.build_context_build_modules = []
        # If specified, the files/targets/variables for the build context will be renamed appending
        # a suffix. It is necessary in case of same require and build_require and will cause an error
        self.build_context_suffix = {}

        # Enable/Disable checking if a component target exists or not
        self.check_components_exist = False
        self._properties = {}

    def generate(self):
        """
        This method will save the generated files to the ``conanfile.generators_folder`` folder
        """
        pass

    @property
    def content(self):
        pass

    def _generate_files(self, require, dep, ret, find_module_mode):
        pass

    def set_property(self, dep, prop, value, build_context=False):
        """
        Using this method you can overwrite the :ref:`property<CMakeDeps Properties>` values set by
        the Conan recipes from the consumer. This can be done for ``cmake_file_name``, ``cmake_target_name``,
        ``cmake_find_mode``, ``cmake_module_file_name``, ``cmake_module_target_name``, ``cmake_additional_variables_prefixes``,
        ``cmake_config_version_compat``, ``system_package_version``,
        ``cmake_build_modules``, ``nosoname``, ``cmake_target_aliases`` and ``cmake_extra_variables``.

        :param dep: Name of the dependency to set the :ref:`property<CMakeDeps Properties>`. For
         components use the syntax: ``dep_name::component_name``.
        :param prop: Name of the :ref:`property<CMakeDeps Properties>`.
        :param value: Value of the property. Use ``None`` to invalidate any value set by the
         upstream recipe.
        :param build_context: Set to ``True`` if you want to set the property for a dependency that
         belongs to the build context (``False`` by default).
        """
        pass

    def get_property(self, prop, dep, comp_name=None, check_type=None):
        pass

    def get_cmake_package_name(self, dep, module_mode=None):
        """Get the name of the file for the ``find_package(XXX)`` call"""
        pass

    def get_find_mode(self, dep):
        """
        :param dep: requirement
        :return: One of ``"none"``, ``"config"``, ``"module"`` or ``"both"``. Defaults to ``"config"`` when not set
        """
        pass

    def generate_aggregator(self):
        pass

    def get_transitive_requires(self, conanfile):
        # Prepared to filter transitive tool-requires with visible=True
        pass
