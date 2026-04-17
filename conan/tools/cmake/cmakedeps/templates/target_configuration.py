import textwrap

from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate

"""

FooTarget-release.cmake

"""


class TargetConfigurationTemplate(CMakeDepsFileTemplate):

    @property
    def filename(self):
        pass

    @property
    def context(self):
        pass

    @property
    def template(self):
        pass

    def get_declared_components_targets_names(self):
        """Returns a list of component_name"""
        pass

    def get_deps_targets_names(self):
        """
          - [{foo}::{bar}, ] of the required
        """
        pass
