import os
import textwrap

import jinja2
from jinja2 import Template

from conan.errors import ConanException
from conan.internal.api.install.generators import relativize_path
from conan.internal.model.pkg_type import PackageType
from conan.internal.graph.graph import CONTEXT_BUILD, CONTEXT_HOST
from conan.tools.cmake.utils import cmake_escape_value


class TargetConfigurationTemplate2:
    """
    FooTarget-release.cmake
    """
    def __init__(self, cmakedeps, conanfile, require, full_cpp_info):
        self._cmakedeps = cmakedeps
        self._conanfile = conanfile  # The dependency conanfile, not the consumer one
        self._require = require
        self._full_cpp_info = full_cpp_info

    def content(self):
        pass

    @property
    def filename(self):
        pass

    def _requires(self, info, components):
        pass

    @property
    def _context(self):
        pass

    def _get_libs(self, cpp_info, pkg_name, pkg_folder, pkg_folder_var) -> dict:
        pass

    def _get_cmake_lib(self, info, components, pkg_folder, pkg_folder_var, comp_name=None):
        pass

    def _get_aliases(self, comp_name=None):
        pass

    def _add_root_lib_target(self, libs, pkg_name, cpp_info):
        """
        Add a new pkgname::pkgname INTERFACE target that depends on default_components or
        on all other library targets (not exes)
        It will not be added if there exists already a pkgname::pkgname target (Or an alias exists).
        """
        pass

    def _get_exes(self, cpp_info, pkg_name, pkg_folder, pkg_folder_var):
        pass

    def _get_dependencies(self):
        """ transitive dependencies Filenames for find_dependency()
        """
        pass

    @staticmethod
    def _path(p, pkg_folder, pkg_folder_var):
        pass

    @property
    def _template(self):
        # TODO: CMake 3.24: Apple Frameworks: https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#genex:LINK_LIBRARY
        # TODO: Check why not set_property instead of target_link_libraries
        pass
