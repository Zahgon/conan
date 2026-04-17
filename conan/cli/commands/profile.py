import json
import os

from conan.api.output import ConanOutput, cli_out_write
from conan.cli.command import conan_command, conan_subcommand
from conan.cli.formatters import default_json_formatter
from conan.cli.args import add_profiles_args
from conan.errors import ConanException


def _print_profiles(profiles):
    pass


def profiles_list_cli_output(profiles):
    pass


def _json_profiles(profiles):
    pass


@conan_subcommand(formatters={"text": _print_profiles, "json": _json_profiles})
def profile_show(conan_api, parser, subparser, *args):
    """
    Show aggregated profiles from the passed arguments.
    """
    pass


@conan_subcommand(formatters={"text": cli_out_write})
def profile_path(conan_api, parser, subparser, *args):
    """
    Show profile path location.
    """
    pass


@conan_subcommand()
def profile_detect(conan_api, parser, subparser, *args):
    """
    Generate a profile using auto-detected values.
    """
    pass


@conan_subcommand(formatters={"text": profiles_list_cli_output, "json": default_json_formatter})
def profile_list(conan_api, parser, subparser, *args):  # noqa
    """
    List all profiles in the cache.
    """
    pass


@conan_command(group="Consumer")
def profile(conan_api, parser, *args):  # noqa
    """
    Manage profiles.
    """
