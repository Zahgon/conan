from jinja2 import Template

from conan.tools import CppInfo
from conan.internal.util.files import save


class SConsDeps:
    def __init__(self, conanfile):
        self._conanfile = conanfile
        self._ordered_deps = None
        self._generator_file = 'SConscript_conandeps'

    @property
    def ordered_deps(self):
        pass

    def _get_cpp_info(self):
        pass

    def generate(self):
        pass

    @property
    def _content(self):
        pass
