import textwrap

from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate

"""

FooTargets.cmake

"""


class TargetsTemplate(CMakeDepsFileTemplate):

    @property
    def filename(self):
        pass

    @property
    def context(self):
        pass

    @property
    def template(self):
        pass
