import os

from conan.internal import check_duplicated_generator
from conan.tools import CppInfo
from conan.tools.env import Environment


def format_defines(defines, toolchain=False):
    pass


class NMakeDeps:

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        self._environment = None

    # TODO: This is similar from AutotoolsDeps: Refactor and make common
    def _get_cpp_info(self):
        pass

    @property
    def environment(self):
        # TODO: Seems we want to make this uniform, equal to other generators
        pass

    def vars(self, scope="build"):
        pass

    def generate(self, scope="build"):
        pass
