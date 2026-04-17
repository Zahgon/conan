import textwrap

import jinja2
from jinja2 import Template

from conan.errors import ConanException


class ConfigVersionTemplate2:
    """
    foo-config-version.cmake
    """
    def __init__(self, cmakedeps, conanfile):
        self._cmakedeps = cmakedeps
        self._conanfile = conanfile

    def content(self):
        pass

    @property
    def filename(self):
        pass

    @property
    def _context(self):
        pass

    @property
    def _template(self):
        # https://gitlab.kitware.com/cmake/cmake/blob/master/Modules/BasicConfigVersion-SameMajorVersion.cmake.in
        # This will be at XXX-config-version.cmake
        # AnyNewerVersion|SameMajorVersion|SameMinorVersion|ExactVersion
        pass
