import textwrap

from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate

"""

cmakedeps_macros.cmake

"""


class MacrosTemplate(CMakeDepsFileTemplate):
    """cmakedeps_macros.cmake"""

    def __init__(self):
        super(MacrosTemplate, self).__init__(cmakedeps=None, require=None, conanfile=None)

    @property
    def filename(self):
        pass

    @property
    def context(self):
        pass

    @property
    def template(self):
        pass
