import os

from conan.internal import check_duplicated_generator
from conan.tools.env import Environment


def runenv_from_cpp_info(dep, os_name):
    """ return an Environment deducing the runtime information from a cpp_info
    """
    pass


class VirtualRunEnv:
    """ Calculates the environment variables of the runtime context and produces a conanrunenv
        .bat or .sh script
    """

    def __init__(self, conanfile, auto_generate=False):
        """

        :param conanfile:  The current recipe object. Always use ``self``.
        """
        self._runenv = None
        self._conanfile = conanfile
        if not auto_generate:
            self._conanfile.virtualrunenv = False
        self.basename = "conanrunenv"
        self.configuration = conanfile.settings.get_safe("build_type")
        if self.configuration:
            self.configuration = self.configuration.lower()
        self.arch = conanfile.settings.get_safe("arch")
        if self.arch:
            self.arch = self.arch.lower()

    @property
    def _filename(self):
        pass

    def environment(self):
        """
        Returns an ``Environment`` object containing the environment variables of the run context.

        :return: an ``Environment`` object instance containing the obtained variables.
        """
        pass

    def vars(self, scope="run"):
        """
        :param scope: Scope to be used.
        :return: An ``EnvVars`` instance containing the computed environment variables.
        """
        pass

    def generate(self, scope="run"):
        """
        Produces the launcher scripts activating the variables for the run context.

        :param scope: Scope to be used.
        """
        pass
