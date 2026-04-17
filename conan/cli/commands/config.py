import os

from conan.api.model import Remote
from conan.api.output import cli_out_write
from conan.cli import make_abs_path
from conan.cli.command import conan_command, conan_subcommand, OnceArgument
from conan.cli.formatters import default_json_formatter
from conan.errors import ConanException


@conan_command(group='Consumer')
def config(conan_api, parser, *args):  # noqa
    """
    Manage the Conan configuration in the Conan home.
    """


@conan_subcommand()
def config_install(conan_api, parser, subparser, *args):
    """
    Install the configuration (remotes, profiles, conf), from git, http or a folder, into the
    Conan home folder.
    """
    pass


@conan_subcommand()
def config_install_pkg(conan_api, parser, subparser, *args):
    """
    (Experimental) Install the configuration (remotes, profiles, conf), from a Conan package
    or from a conanconfig.yml file
    """
    pass


def _list_text_formatter(confs):
    pass


@conan_subcommand(formatters={"text": cli_out_write})
def config_home(conan_api, parser, subparser, *args):  # noqa
    """
    Show the Conan home folder.
    """
    pass


@conan_subcommand(formatters={"text": _list_text_formatter, "json": default_json_formatter})
def config_list(conan_api, parser, subparser, *args):
    """
    Show all the Conan available configurations: core and tools.
    """
    pass


@conan_subcommand(formatters={"text": _list_text_formatter, "json": default_json_formatter})
def config_show(conan_api, parser, subparser, *args):
    """
    Get the value of the specified conf
    """
    pass


@conan_subcommand()
def config_clean(conan_api, parser, subparser, *args):  # noqa
    """
    (Experimental) Clean the configuration files in the Conan home folder, while keeping
    installed packages
    """
    pass
