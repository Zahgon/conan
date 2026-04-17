import argparse
import os
import textwrap
from contextlib import redirect_stdout

from conan.api.output import ConanOutput
from conan.errors import ConanException


class OnceArgument(argparse.Action):
    """Allows declaring a parameter that can have only one value, by default argparse takes the
    latest declared and it's very confusing.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None and self.default is None:
            msg = '{o} can only be specified once'.format(o=option_string)
            raise argparse.ArgumentError(None, msg)
        setattr(namespace, self.dest, values)


class SmartFormatter(argparse.HelpFormatter):

    def _fill_text(self, text, width, indent):
        pass


class BaseConanCommand:
    def __init__(self, method, formatters=None):
        self._formatters = {"text": lambda x: None}
        self._method = method
        self._name = None
        if formatters:
            for kind, action in formatters.items():
                if callable(action):
                    self._formatters[kind] = action
                else:
                    raise ConanException("Invalid formatter for {}. The formatter must be"
                                         " a valid function".format(kind))
        if method.__doc__:
            self._doc = method.__doc__
        else:
            raise ConanException("No documentation string defined for command: '{}'. Conan "
                                 "commands should provide a documentation string explaining "
                                 "its use briefly.".format(self._name))

    @staticmethod
    def _init_core_options(parser):
        # Define possible levels, including "" for verbose
        pass

    @property
    def _help_formatters(self):
        """
        Formatters that are shown as available in help, 'text' formatter
        should not appear
        """
        pass

    def _init_formatters(self, parser):
        pass

    @property
    def name(self):
        pass

    @property
    def method(self):
        pass

    @property
    def doc(self):
        pass

    def _format(self, parser, info, *args):
        pass

    @staticmethod
    def _dispatch_errors(info):
        pass


class ConanArgumentParser(argparse.ArgumentParser):

    def __init__(self, conan_api, *args, **kwargs):
        self._conan_api = conan_api
        super().__init__(*args, **kwargs)

    def parse_args(self, args=None, namespace=None):
        pass


class ConanCommand(BaseConanCommand):
    def __init__(self, method, group=None, formatters=None):
        super().__init__(method, formatters=formatters)
        self._subcommands = {}
        self._group = group or "Other"
        self._name = method.__name__.replace("_", "-")
        self._prog = self._name

    def add_subcommand(self, subcommand):
        pass

    def run_cli(self, conan_api, *args):
        pass

    def run(self, conan_api, *args):
        pass

    @property
    def group(self):
        pass


class ConanSubCommand(BaseConanCommand):
    def __init__(self, method, formatters=None):
        super().__init__(method, formatters=formatters)
        self._parser = None
        self._subcommand_name = method.__name__.replace('_', '-')

    def run_cli(self, conan_api, parent_parser, *args):
        pass

    def run(self, conan_api, parent_parser, *args):
        pass

    def set_name(self, parent_name):
        pass

    def set_parser(self, subcommand_parser, conan_api):
        pass


def conan_command(group=None, formatters=None):
    return lambda f: ConanCommand(f, group, formatters=formatters)


def conan_subcommand(formatters=None):
    return lambda f: ConanSubCommand(f, formatters=formatters)
