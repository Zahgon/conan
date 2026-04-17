import textwrap
from io import StringIO

from conan.tools.build import cmd_args_to_string
from conan.tools.env import Environment
from conan.errors import ConanException


class PkgConfig:

    def __init__(self, conanfile, library, pkg_config_path=None):
        """

        :param conanfile: The current recipe object. Always use ``self``.
        :param library: The library which ``.pc`` file is to be parsed. It must exist in the pkg_config path.
        :param pkg_config_path:  If defined it will be prepended to ``PKG_CONFIG_PATH`` environment
               variable, so the execution finds the required files.
        """
        self._conanfile = conanfile
        self._library = library
        self._info = {}
        self._pkg_config_path = pkg_config_path
        self._variables = None

    def _parse_output(self, option):
        pass

    def _get_option(self, option):
        pass

    @property
    def includedirs(self):
        pass

    @property
    def cflags(self):
        pass

    @property
    def defines(self):
        pass

    @property
    def libdirs(self):
        pass

    @property
    def libs(self):
        pass

    @property
    def linkflags(self):
        pass

    @property
    def provides(self):
        pass

    @property
    def version(self):
        pass

    @property
    def variables(self):
        pass

    def fill_cpp_info(self, cpp_info, is_system=True, system_libs=None):
        """
        Method to fill a cpp_info object from the PkgConfig configuration

        :param cpp_info: Can be the global one (self.cpp_info) or a component one (self.components["foo"].cpp_info).
        :param is_system: If ``True``, all detected libraries will be assigned to ``cpp_info.system_libs``, and none to ``cpp_info.libs``.
        :param system_libs: If ``True``, all detected libraries will be assigned to ``cpp_info.system_libs``, and none to ``cpp_info.libs``.

        """
        pass
