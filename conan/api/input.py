import getpass
import sys

from conan.errors import ConanException


class UserInput:
    """Class to interact with the user, used to show messages and ask for information"""

    def __init__(self, non_interactive):
        """
        Params:
            ins: input stream
            out: ConanOutput, should have "write" method
        """
        self._ins = sys.stdin
        # FIXME: circular include, move "color_enabled" function to better location
        from conan.api.output import ConanOutput
        self._out = ConanOutput()
        self._interactive = not non_interactive

    def _raise_if_non_interactive(self):
        pass

    def raw_input(self):
        pass

    def request_login(self, remote_name, username=None):
        """Request user to input their name and password
        :param remote_name:
        :param username If username is specified it only request password"""
        pass

    def get_username(self):
        """Overridable for testing purpose"""
        pass

    @staticmethod
    def get_password():
        """Overridable for testing purpose"""
        pass

    def request_string(self, msg, default_value=None):
        """Request user to input a msg
        :param default_value:
        :param msg Name of the msg
        """
        pass

    def request_boolean(self, msg, default_option=None):
        """Request user to input a boolean"""
        pass
