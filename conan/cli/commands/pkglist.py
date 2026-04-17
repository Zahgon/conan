from conan.api.conan_api import ConanAPI
from conan.api.model import MultiPackagesList
from conan.cli import make_abs_path
from conan.cli.command import conan_command, conan_subcommand
from conan.cli.commands.list import print_list_text, print_list_json
from conan.cli.formatters.list import list_packages_html


@conan_command(group="Consumer")
def pkglist(conan_api: ConanAPI, parser, *args):  # noqa
    """
    Several operations over package lists
    """


@conan_subcommand(formatters={"text": print_list_text,
                              "json": print_list_json,
                              "html": list_packages_html})
def pkglist_find_remote(conan_api, parser, subparser, *args):
    """
    (Experimental) Find the remotes of a list of packages in the cache
    """
    pass


@conan_subcommand(formatters={"text": print_list_text,
                              "json": print_list_json,
                              "html": list_packages_html})
def pkglist_merge(conan_api, parser, subparser, *args):
    """
    (Experimental) Merge several package lists into a single one
    """
    pass
