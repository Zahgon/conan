import os

from conan.cli.formatters.report import format_diff_html, format_diff_txt, format_diff_json
from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command, conan_subcommand


@conan_command(group="Security")
def report(conan_api: ConanAPI, parser, *args):
    """
    Gets information about the recipe and its sources.
    """


@conan_subcommand(formatters={"text": format_diff_txt,
                              "json": format_diff_json,
                              "html": format_diff_html})
def report_diff(conan_api, parser, subparser, *args):
    """
    Get the difference between two recipes with their sources.
    It can be used to compare two different versions of the same recipe, or two different recipe revisions.

    Each old/new recipe can be specified by a path to a conanfile.py and a companion reference,
    or by a reference only.

    If only a reference is specified, it will be searched in the local cache,
    or downloaded from the specified remotes. If no revision is specified, the latest revision will be used.
    """
    pass
