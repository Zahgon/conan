from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, MultiPackagesList
from conan.api.output import ConanOutput
from conan.cli import make_abs_path
from conan.cli.command import conan_command, OnceArgument
from conan.cli.commands.list import print_list_text, print_list_json
from conan.errors import ConanException


@conan_command(group="Creator", formatters={"text": print_list_text,
                                            "json": print_list_json})
def download(conan_api: ConanAPI, parser, *args):
    """
    Download (without installing) a single conan package from a remote server.

    It downloads just the package, but not its transitive dependencies, and it will not call
    any generate, generators or deployers.
    It can download multiple packages if patterns are used, and also works with
    queries over the package binaries.
    """
    pass
