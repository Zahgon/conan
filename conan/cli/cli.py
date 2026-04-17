import importlib
import os
import pkgutil
import re
import signal
import sys
import textwrap
import traceback
from collections import defaultdict
from difflib import get_close_matches
from inspect import getmembers

from conan.api.conan_api import ConanAPI
from conan.api.output import ConanOutput, Color, cli_out_write, LEVEL_TRACE
from conan.cli.command import ConanSubCommand
from conan.cli.exit_codes import SUCCESS, ERROR_MIGRATION, ERROR_GENERAL, USER_CTRL_C, \
    ERROR_SIGTERM, USER_CTRL_BREAK, ERROR_INVALID_CONFIGURATION, ERROR_UNEXPECTED
from conan import __version__
from conan.errors import ConanException, ConanInvalidConfiguration, ConanMigrationError

_CONAN_INTERNAL_CUSTOM_COMMANDS_PATH = "_CONAN_INTERNAL_CUSTOM_COMMANDS_PATH"


class Cli:
    """A single command of the conan application, with all the first level commands. Manages the
    parsing of parameters and delegates functionality to the conan python api. It can also show the
    help of the tool.
    """
    _builtin_commands = None  # Caching the builtin commands, no need to load them over and over

    def __init__(self, conan_api):
        assert isinstance(conan_api, ConanAPI), \
            "Expected 'Conan' type, got '{}'".format(type(conan_api))
        self._conan_api = conan_api
        self._conan_api.command.cli = self
        self._groups = defaultdict(list)
        self._commands = {}

    def add_commands(self):
        pass

    def _add_command(self, import_path, method_name, package=None):
        pass

    def _print_similar(self, command):
        """ Looks for similar commands and prints them if found.
        """
        pass

    def _output_help_cli(self):
        """
        Prints a summary of all commands.
        """
        pass

    def run(self, *args):
        """ Entry point for executing commands, dispatcher to class
        methods
        """
        pass

    @staticmethod
    def _conan2_migrate_recipe_msg(exception):
        pass

    @staticmethod
    def exception_exit_error(exception):
        pass


def _warn_frozen_center(conan_api):
    pass


def main(args):
    """ main entry point of the conan application, using a Command to
    parse parameters

    Exit codes for conan command:

        0: Success (done)
        1: General ConanException error (done)
        2: Migration error
        3: Ctrl+C
        4: Ctrl+Break
        5: SIGTERM
        6: Invalid configuration (done)
    """
    pass


def _warn_python_version():
    pass
