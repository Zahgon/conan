import json
import os

from conan.api.model import MultiPackagesList, PackagesList
from conan.api.output import cli_out_write
from conan.cli.command import conan_command, OnceArgument
from conan.cli.args import add_reference_args


def common_args_export(parser):
    pass


def json_export(data):
    pass


def pkglist_export(data):
    pass


@conan_command(group="Creator", formatters={"json": json_export, "pkglist": pkglist_export})
def export(conan_api, parser, *args):
    """
    Export a recipe to the Conan package cache.
    """
    pass
