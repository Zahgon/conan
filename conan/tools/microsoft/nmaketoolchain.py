
from conan.internal import check_duplicated_generator
from conan.tools.build.flags import build_type_flags, cppstd_flag, build_type_link_flags
from conan.tools.env import Environment
from conan.tools.microsoft.nmakedeps import format_defines
from conan.tools.microsoft.visual import msvc_runtime_flag, VCVars


class NMakeToolchain:
    """
    https://learn.microsoft.com/en-us/cpp/build/reference/running-nmake?view=msvc-170#toolsini-and-nmake
    We have also explored the usage of Tools.ini:
    https://learn.microsoft.com/en-us/cpp/build/reference/running-nmake?view=msvc-170
    but not possible, because it cannot include other files, it will also potentially collide with
    a user Tool.ini, without easy resolution. At least the environment is additive.
    """
    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile

        # Flags
        self.extra_cflags = []
        self.extra_cxxflags = []
        self.extra_ldflags = []
        self.extra_defines = []

    @staticmethod
    def _format_options(options):
        pass

    @property
    def _cl(self):
        pass

    @property
    def _link(self):
        pass

    @property
    def _rcflags(self):
        pass

    def environment(self):
        pass

    def vars(self):
        pass

    def generate(self, env=None, scope="build"):
        pass
