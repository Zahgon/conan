import textwrap

from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate

"""

FooConfig.cmake
foo-config.cmake

"""


class ConfigTemplate(CMakeDepsFileTemplate):

    @property
    def filename(self):
        pass

    @property
    def additional_variables_prefixes(self):
        pass

    @property
    def parsed_extra_variables(self):
        # Reading configuration from "cmake_extra_variables" property
        pass

    @property
    def context(self):
        pass

    @property
    def template(self):
        pass
