from conan.internal import check_duplicated_generator
from conan.tools import CppInfo
from conan.tools.env import Environment
from conan.tools.gnu.gnudeps_flags import GnuDepsFlags


class AutotoolsDeps:
    def __init__(self, conanfile):
        self._conanfile = conanfile
        self._environment = None
        self._ordered_deps = None

    @property
    def ordered_deps(self):
        pass

    def _get_cpp_info(self):
        pass

    def _rpaths_flags(self):
        pass

    @property
    def environment(self):
        """

        :return: An ``Environment`` object containing the computed variables. If you need
                 to modify some of the computed values you can access to the ``environment`` object.
        """
        pass

    def vars(self, scope="build"):
        pass

    def generate(self,  scope="build"):
        pass
