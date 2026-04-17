import json
import os
from collections import OrderedDict

from conan.api.conan_api import ConanAPI
from conan.api.model import Remote, LOCAL_RECIPES_INDEX
from conan.api.output import cli_out_write, Color
from conan.cli import make_abs_path
from conan.cli.command import conan_command, conan_subcommand, OnceArgument
from conan.cli.commands.list import remote_color, error_color, recipe_color, \
    reference_color
from conan.errors import ConanException


def _print_remotes_json(remotes):
    pass


def _print_remote_list(remotes):
    pass


def _print_remote_user_list(results):
    pass


def _print_remote_user_set(results):
    pass


def _print_remotes_users_json(results):
    pass


@conan_subcommand(formatters={"text": _print_remote_list, "json": _print_remotes_json})
def remote_list(conan_api: ConanAPI, parser, subparser, *args):  # noqa
    """
    List current remotes.
    """
    pass


@conan_subcommand()
def remote_add(conan_api, parser, subparser, *args):
    """
    Add a remote.
    """
    pass


@conan_subcommand(formatters={"text": _print_remote_list})
def remote_remove(conan_api, parser, subparser, *args):
    """
    Remove remotes.
    """
    pass


@conan_subcommand()
def remote_update(conan_api, parser, subparser, *args):
    """
    Update a remote.
    """
    pass


@conan_subcommand()
def remote_rename(conan_api, parser, subparser, *args):
    """
    Rename a remote.
    """
    pass


@conan_subcommand(formatters={"text": _print_remote_list, "json": _print_remotes_json})
def remote_enable(conan_api, parser, subparser, *args):
    """
    Enable all the remotes matching a pattern.
    """
    pass


@conan_subcommand(formatters={"text": _print_remote_list, "json": _print_remotes_json})
def remote_disable(conan_api, parser, subparser, *args):
    """
    Disable all the remotes matching a pattern.
    """
    pass


# ### User related commands

@conan_subcommand(formatters={"text": _print_remote_user_list, "json": _print_remotes_users_json})
def remote_list_users(conan_api, parser, subparser, *args):  # noqa
    """
    List the users logged into all the remotes.
    """
    pass


@conan_subcommand(formatters={"text": _print_remote_user_set, "json": _print_remotes_users_json})
def remote_login(conan_api, parser, subparser, *args):
    """
    Login into the specified remotes matching a pattern.
    """
    pass


@conan_subcommand(formatters={"text": _print_remote_user_set, "json": _print_remotes_users_json})
def remote_set_user(conan_api, parser, subparser, *args):
    """
    Associate a username with a remote matching a pattern without performing the authentication.
    """
    pass


@conan_subcommand(formatters={"text": _print_remote_user_set, "json": _print_remotes_users_json})
def remote_logout(conan_api, parser, subparser, *args):
    """
    Clear the existing credentials for the specified remotes matching a pattern.
    """
    pass


def _print_auth(remotes):
    pass


def _print_auth_json(results):
    pass


@conan_subcommand(formatters={"text": _print_auth, "json": _print_auth_json})
def remote_auth(conan_api, parser, subparser, *args):
    """
    Authenticate in the defined remotes. Use CONAN_LOGIN_USERNAME* and CONAN_PASSWORD* variables
    if available.
    Ask for username and password interactively in case (re-)authentication is required and there are
    no CONAN_LOGIN* and CONAN_PASSWORD* variables available which could be used.
    Usually you'd use this method over conan remote login for scripting which needs to run in CI
    and locally.
    By default, this command returns exit code 0 even if authentication fails for some remotes.
    Use --strict to return exit code 1 if authentication fails for any remote.
    """
    pass


@conan_command(group="Consumer")
def remote(conan_api, parser, *args):  # noqa
    """
    Manage the remote list and the users authenticated on them.
    """
