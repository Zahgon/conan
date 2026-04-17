import os
import shlex

from conan.api.output import ConanOutput
from conan.errors import ConanException


class CommandAPI:
    """ This CommandAPI is useful to be able to launch full commands from the ConanAPI

    Sometimes some commands are built using several calls to the ConanAPI. If we want
    to reuse the same functionality, then we would have to copy all that code into our
    own commands.
    Instead of doing that, it is possible to call Conan commands using this API, via
    the ``run()`` method.
    """

    def __init__(self, conan_api):
        self._conan_api = conan_api
        self.cli = None

    def run(self, cmd):
        """ Runs another Conan command via API

        :param cmd: Conan command to run. It can be either a string, or a list of strings.
        :return: It will return what that command returns. Note that different commands can
           return different things, so the caller needs to process it accordingly.
        """
        pass

    @staticmethod
    def get_runner(profile_host):
        pass
