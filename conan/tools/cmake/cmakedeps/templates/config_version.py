import textwrap

from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate
from conan.errors import ConanException

"""
    foo-config-version.cmake

"""


class ConfigVersionTemplate(CMakeDepsFileTemplate):

    @property
    def filename(self):
        pass

    @property
    def context(self):
        pass

    @property
    def template(self):
        # https://gitlab.kitware.com/cmake/cmake/blob/master/Modules/BasicConfigVersion-SameMajorVersion.cmake.in
        # This will be at XXX-config-version.cmake
        # AnyNewerVersion|SameMajorVersion|SameMinorVersion|ExactVersion
        pass
