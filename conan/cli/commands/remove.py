from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, MultiPackagesList, PackagesList
from conan.api.output import cli_out_write, ConanOutput
from conan.api.input import UserInput
from conan.cli import make_abs_path
from conan.cli.command import conan_command, OnceArgument
from conan.cli.commands.list import print_list_json, print_serial
from conan.errors import ConanException


def summary_remove_list(results):
    """ Do a little format modification to serialized
    package list so it looks prettier on text output
    """
    pass


@conan_command(group="Consumer", formatters={"text": summary_remove_list,
                                             "json": print_list_json})
def remove(conan_api: ConanAPI, parser, *args):
    """
    Remove recipes or packages from local cache or a remote.

    - If no remote is specified (-r), the removal will be done in the local conan cache.
    - If a recipe reference is specified, it will remove the recipe and all the packages, unless -p
      is specified, in that case, only the packages matching the specified query (and not the recipe)
      will be removed.
    - If a package reference is specified, it will remove only the package.
    """
    pass
