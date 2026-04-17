import json
import os

from conan.api.output import ConanOutput, cli_out_write
from conan.cli.args import add_reference_args
from conan.cli.command import conan_command, conan_subcommand


@conan_command(group="Creator")
def editable(conan_api, parser, *args):
    """
    Allow working with a package that resides in user folder.
    """


@conan_subcommand()
def editable_add(conan_api, parser, subparser, *args):
    """
    Define the given <path> location as the package <reference>, so when this
    package is required, it is used from this <path> location instead of the cache.
    """
    pass


@conan_subcommand()
def editable_remove(conan_api, parser, subparser, *args):
    """
    Remove the "editable" mode for this reference.
    """
    pass


def print_editables_json(data):
    pass


def print_editables_text(data):
    pass


@conan_subcommand(formatters={"text": print_editables_text, "json": print_editables_json})
def editable_list(conan_api, parser, subparser, *args):
    """
    List all the packages in editable mode.
    """
    pass
