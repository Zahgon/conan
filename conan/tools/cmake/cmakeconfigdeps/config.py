import textwrap

import jinja2
from jinja2 import Template
from conan.tools.cmake.utils import parse_extra_variable, cmake_escape_value
from conan.internal.api.install.generators import relativize_path


class ConfigTemplate2:
    """
    FooConfig.cmake
    foo-config.cmake
    """
    def __init__(self, cmakedeps, require, conanfile, full_cpp_info):
        self._cmakedeps = cmakedeps
        self._require = require
        self._conanfile = conanfile
        self._full_cpp_info = full_cpp_info

    def content(self):
        pass

    @property
    def filename(self):
        pass

    @property
    def _context(self):
        pass

    def _get_legacy_vars(self):
        # Auxiliary variables for legacy consumption and try_compile cases
        pass

    @property
    def _template(self):
        pass
