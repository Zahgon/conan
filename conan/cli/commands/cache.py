import json

from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, MultiPackagesList
from conan.api.output import cli_out_write, ConanOutput
from conan.cli import make_abs_path
from conan.cli.command import conan_command, conan_subcommand, OnceArgument
from conan.cli.commands.list import print_list_text, print_list_json, print_serial
from conan.errors import ConanException
from conan.api.model import PkgReference
from conan.api.model import RecipeReference


def _get_package_sign_error(pkg_list):
    pass


def print_package_sign_text(data):
    pass


def json_export(data):
    pass


@conan_command(group="Consumer")
def cache(conan_api: ConanAPI, parser, *args):
    """
    Perform file operations in the local cache (of recipes and/or packages).
    """
    pass


@conan_subcommand(formatters={"text": cli_out_write, "json": json_export})
def cache_path(conan_api: ConanAPI, parser, subparser, *args):
    """
    Show the path to the Conan cache for a given reference.
    """
    pass


@conan_subcommand(formatters={"text": cli_out_write})
def cache_ref(conan_api: ConanAPI, parser, subparser, *args):
    """
    Show the reference for a given Conan cache folder
    """
    pass


@conan_subcommand()
def cache_clean(conan_api: ConanAPI, parser, subparser, *args):
    """
    Remove non-critical folders from the cache, like source, build and/or download
    (.tgz store) ones.
    """
    pass


def print_list_check_integrity_json(data):
    pass


@conan_subcommand(formatters={"text": lambda _: (),
                              "json": print_list_check_integrity_json})
def cache_check_integrity(conan_api: ConanAPI, parser, subparser, *args):
    """
    Check the integrity of the local cache for the given references
    """
    pass

@conan_subcommand(formatters={"text": print_package_sign_text,
                              "json": print_list_json})
def cache_sign(conan_api: ConanAPI, parser, subparser, *args):
    """
    Sign packages with the Package Signing Plugin
    """
    pass


@conan_subcommand(formatters={"text": print_package_sign_text,
                              "json": print_list_json})
def cache_verify(conan_api: ConanAPI, parser, subparser, *args):
    """
    Check the signature of packages with the Package Signing Plugin
    """
    pass


@conan_subcommand(formatters={"text": print_list_text,
                              "json": print_list_json})
def cache_save(conan_api: ConanAPI, parser, subparser, *args):
    """
    Get the artifacts from a package list and archive them
    """
    pass


@conan_subcommand(formatters={"text": print_list_text,
                              "json": print_list_json})
def cache_restore(conan_api: ConanAPI, parser, subparser, *args):
    """
    Put  the artifacts from an archive into the cache
    """
    pass


@conan_subcommand()
def cache_backup_upload(conan_api: ConanAPI, parser, subparser, *args):
    """
    Upload all the source backups present in the cache
    """
    pass
