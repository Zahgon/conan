import textwrap

import jinja2
from jinja2 import Template


class TargetsTemplate2:
    """
    FooTargets.cmake
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
        pass
