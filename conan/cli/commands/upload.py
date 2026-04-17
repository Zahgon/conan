from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, MultiPackagesList, PackagesList
from conan.api.output import ConanOutput
from conan.cli import make_abs_path
from conan.cli.command import conan_command, OnceArgument
from conan.cli.commands.list import print_list_json, print_serial
from conan.api.input import UserInput
from conan.errors import ConanException


def summary_upload_list(results):
    """ Do a little format modification to serialized
    package list, so it looks prettier on text output
    """
    pass


@conan_command(group="Creator", formatters={"text": summary_upload_list,
                                            "json": print_list_json})
def upload(conan_api: ConanAPI, parser, *args):
    """
    Upload packages to a remote.

    By default, all the matching references are uploaded (all revisions).
    By default, if a recipe reference is specified, it will upload all the revisions for all the
    binary packages, unless --only-recipe is specified. You can use the "latest" placeholder at the
    "reference" argument to specify the latest revision of the recipe or the package.
    """
    pass


def _ask_confirm_upload(conan_api, package_list):
    pass
