import json
import os

from conan.api.output import ConanOutput, cli_out_write, Color
from conan.cli import make_abs_path
from conan.cli.args import common_graph_args, validate_common_graph_args
from conan.cli.command import conan_command, conan_subcommand
from conan.cli.commands.list import prepare_pkglist_compact, print_serial
from conan.cli.formatters.graph import format_graph_html, format_graph_json, format_graph_dot
from conan.cli.formatters.graph.build_order_html import format_build_order_html
from conan.cli.formatters.graph.graph_info_text import format_graph_info
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_packages, print_graph_basic
from conan.errors import ConanException


def explain_formatter_text(data):
    pass


def explain_formatter_json(data):
    pass


@conan_command(group="Consumer")
def graph(conan_api, parser, *args):  # noqa
    """
    Compute a dependency graph, without installing or building the binaries.
    """


def cli_build_order(result):
    # TODO: Very simple cli output, probably needs to be improved
    pass


def json_build_order(result):
    pass


@conan_subcommand(formatters={"text": cli_build_order, "json": json_build_order,
                              "html": format_build_order_html})
def graph_build_order(conan_api, parser, subparser, *args):
    """
    Compute the build order of a dependency graph.
    """
    pass


@conan_subcommand(formatters={"text": cli_build_order, "json": json_build_order,
                              "html": format_build_order_html})
def graph_build_order_merge(conan_api, parser, subparser, *args):  # noqa
    """
    Merge more than 1 build-order file.
    """
    pass


@conan_subcommand(formatters={"text": format_graph_info,
                              "html": format_graph_html,
                              "json": format_graph_json,
                              "dot": format_graph_dot})
def graph_info(conan_api, parser, subparser, *args):
    """
    Compute the dependency graph and show information about it.
    """
    pass


@conan_subcommand(formatters={"text": explain_formatter_text,
                              "json": explain_formatter_json})
def graph_explain(conan_api, parser,  subparser, *args):
    """
    Explain what is wrong with the dependency graph, like report missing binaries closest
    alternatives, trying to explain why the existing binaries do not match
    """
    pass


def outdated_text_formatter(result):
    pass


def outdated_json_formatter(result):
    pass


@conan_subcommand(formatters={"text": outdated_text_formatter, "json": outdated_json_formatter})
def graph_outdated(conan_api, parser, subparser, *args):
    """
    List the dependencies in the graph and it's newer versions in the remote
    """
    pass
