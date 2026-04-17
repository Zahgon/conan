import json
import os

from conan.api.conan_api import ConanAPI
from conan.api.model import RecipeReference
from conan.api.output import ConanOutput, cli_out_write
from conan.api.subapi.workspace import WorkspaceAPI
from conan.cli import make_abs_path
from conan.cli.args import add_reference_args, add_common_install_arguments, add_lockfile_args
from conan.cli.command import conan_command, conan_subcommand, OnceArgument
from conan.cli.commands.list import print_serial
from conan.cli.formatters.graph import format_graph_json
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_packages, print_graph_basic
from conan.errors import ConanException
from conan.internal.graph.install_graph import ProfileArgs


@conan_subcommand(formatters={"text": cli_out_write})
def workspace_root(conan_api: ConanAPI, parser, subparser, *args):  # noqa
    """
    Return the folder containing the conanws.py/conanws.yml workspace file
    """
    pass


@conan_subcommand()
def workspace_open(conan_api: ConanAPI, parser, subparser, *args):
    """
    Open specific references
    """
    pass


@conan_subcommand()
def workspace_add(conan_api: ConanAPI, parser, subparser, *args):
    """
    Add packages to current workspace
    """
    pass


@conan_subcommand()
def workspace_complete(conan_api: ConanAPI, parser, subparser, *args):
    """
    Complete the workspace, opening or adding intermediate packages to it that have
    requirements to other packages in the workspace.
    """
    pass


@conan_subcommand()
def workspace_remove(conan_api: ConanAPI, parser, subparser, *args):
    """
    Remove packages from the current workspace
    """
    pass


def _print_json(data):
    pass


def _print_workspace_info(data):
    pass


@conan_subcommand(formatters={"text": _print_workspace_info, "json": _print_json})
def workspace_info(conan_api: ConanAPI, parser, subparser, *args):  # noqa
    """
    Display info for current workspace
    """
    pass


@conan_subcommand()
def workspace_build(conan_api: ConanAPI, parser, subparser, *args):
    """
    Call "conan build" for packages in the workspace, in the right order
    """
    pass


@conan_subcommand()
def workspace_install(conan_api: ConanAPI, parser, subparser, *args):
    """
    Call "conan install" for packages in the workspace, in the right order
    """
    pass


def _install_build(conan_api: ConanAPI, parser, subparser, build, *args):
    pass


@conan_subcommand(formatters={"json": format_graph_json})
def workspace_super_install(conan_api: ConanAPI, parser, subparser, *args):
    """
    Install the workspace as a monolith, installing only external dependencies to the workspace,
    generating a single result (generators, etc) for the whole workspace.
    """
    pass


@conan_subcommand()
def workspace_clean(conan_api: ConanAPI, parser, subparser, *args):  # noqa
    """
    Clean the temporary build folders when possible
    """
    pass


@conan_subcommand()
def workspace_init(conan_api: ConanAPI, parser, subparser, *args):
    """
    Clean the temporary build folders when possible
    """
    pass


@conan_subcommand()
def workspace_create(conan_api: ConanAPI, parser, subparser, *args):
    """
    Call "conan create" for packages in the workspace, in the correct order.
    Packages will be created in the Conan cache, not locally
    """
    pass


@conan_subcommand()
def workspace_source(conan_api: ConanAPI, parser, subparser, *args):
    """
    Call the source() method of packages in the workspace
    """
    pass


@conan_command(group="Consumer")
def workspace(conan_api, parser, *args):  # noqa
    """
    Manage Conan workspaces (group of packages in editable mode)
    """
    pass
