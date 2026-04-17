from conan.internal import check_duplicated_generator
from conan.tools.env import Environment
from conan.tools.env.virtualrunenv import runenv_from_cpp_info


class VirtualBuildEnv:
    """ Calculates the environment variables of the build time context and produces a conanbuildenv
        .bat or .sh script
    """

    def __init__(self, conanfile, auto_generate=False):
        self._buildenv = None
        self._conanfile = conanfile
        if not auto_generate:
            self._conanfile.virtualbuildenv = False
        self.basename = "conanbuildenv"
        self.configuration = None
        self.arch = None

    @property
    def _filename(self):
        pass

    def environment(self):
        """
        Returns an ``Environment`` object containing the environment variables of the build context.

        :return: an ``Environment`` object instance containing the obtained variables.
        """
        pass

    def vars(self, scope="build"):
        """
        :param scope: Scope to be used.
        :return: An ``EnvVars`` instance containing the computed environment variables.
        """
        pass

    def generate(self, scope="build"):
        """
        Produces the launcher scripts activating the variables for the build context.

        :param scope: Scope to be used.
        """
        pass
