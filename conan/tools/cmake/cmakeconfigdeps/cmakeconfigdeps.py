import glob
import os
import re
import textwrap

from jinja2 import Template

from conan.api.output import Color, ConanOutput
from conan.errors import ConanException
from conan.internal import check_duplicated_generator
from conan.internal.api.install.generators import relativize_path
from conan.internal.model.dependencies import get_transitive_requires
from conan.tools.cmake.cmakeconfigdeps.config import ConfigTemplate2
from conan.tools.cmake.cmakeconfigdeps.config_version import ConfigVersionTemplate2
from conan.tools.cmake.cmakeconfigdeps.target_configuration import TargetConfigurationTemplate2
from conan.tools.cmake.cmakeconfigdeps.targets import TargetsTemplate2
from conan.tools.files import save
from conan.internal.util.files import load

FIND_MODE_MODULE = "module"
FIND_MODE_CONFIG = "config"
FIND_MODE_NONE = "none"
FIND_MODE_BOTH = "both"


class CMakeConfigDeps:

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        self.configuration = str(self._conanfile.settings.build_type)

        # These are just for legacy compatibility, but not use at al
        self._build_context_activated = []
        self._build_context_build_modules = []
        self._build_context_suffix = {}
        # Enable/Disable checking if a component target exists or not
        self._check_components_exist = False

        self._properties = {}

    @property
    def build_context_activated(self):
        pass

    @build_context_activated.setter
    def build_context_activated(self, value):
        pass

    @property
    def build_context_build_modules(self):
        pass

    @build_context_build_modules.setter
    def build_context_build_modules(self, value):
        pass

    @property
    def build_context_suffix(self):
        pass

    @build_context_suffix.setter
    def build_context_suffix(self, value):
        pass

    @property
    def check_components_exist(self):
        pass

    @check_components_exist.setter
    def check_components_exist(self, value):
        pass

    def generate(self):
        """
        This method will save the generated files to the ``conanfile.generators_folder`` folder
        """
        pass

    def _content(self):
        pass

    def _print_help(self, direct_deps):
        pass

    def set_property(self, dep, prop, value, build_context=False):
        """
        Using this method you can overwrite the :ref:`property<CMakeConfigDeps Properties>` values
        set by the Conan recipes from the consumer.

        :param dep: Name of the dependency to set the :ref:`property<CMakeConfigDeps Properties>`.
         For components use the syntax: ``dep_name::component_name``.
        :param prop: Name of the :ref:`property<CMakeDeps Properties>`.
        :param value: Value of the property. Use ``None`` to invalidate any value set by the
         upstream recipe.
        :param build_context: Set to ``True`` if you want to set the property for a dependency that
         belongs to the build context (``False`` by default).
        """
        pass

    def get_property(self, prop, dep, comp_name=None, check_type=None):
        pass

    def get_cmake_filename(self, dep):
        # Get the name of the file for the find_package(XXX)
        # This is used by CMakeDeps to determine:
        # - The filename to generate (XXX-config.cmake or FindXXX.cmake)
        # - The name of the defined XXX_DIR variables
        # - The name of transitive dependencies for calls to find_dependency
        pass

    def _get_find_mode(self, dep):
        pass

    def get_transitive_requires(self, conanfile):
        # Prepared to filter transitive tool-requires with visible=True
        pass


# TODO: Repeated from CMakeToolchain blocks
def _join_paths(conanfile, paths):
    pass


class _PathGenerator:
    _conan_cmakedeps_paths = "conan_cmakedeps_paths.cmake"

    def __init__(self, cmakedeps, conanfile):
        self._conanfile = conanfile
        self._cmakedeps = cmakedeps

    def _get_cmake_paths(self, requirements, dirs_name):
        pass

    def generate(self):
        pass

    def _get_host_runtime_dirs(self):
        pass
