import json
import datetime

from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, MultiPackagesList
from conan.api.output import Color, cli_out_write
from conan.cli import make_abs_path
from conan.cli.command import conan_command, OnceArgument
from conan.cli.formatters.list import list_packages_html
from conan.errors import ConanException

# Keep them so we don't break other commands that import them, but TODO: Remove later
remote_color = Color.BRIGHT_BLUE
recipe_name_color = Color.GREEN
recipe_color = Color.BRIGHT_WHITE
reference_color = Color.WHITE
error_color = Color.BRIGHT_RED
field_color = Color.BRIGHT_YELLOW
value_color = Color.CYAN


def _format_timestamp_human(timestamp):
    # used by ref.repr_humantime() to print human readable time
    pass


def print_serial(item, indent=None, color_index=None):
    pass


def print_list_text(results):
    """ Do a little format modification to serialized
    package list, so it looks prettier on text output
    """
    pass


def print_list_compact(results):
    pass


def prepare_pkglist_compact(pkglist):
    pass


def print_list_json(data):
    pass


@conan_command(group="Consumer", formatters={"text": print_list_text,
                                             "json": print_list_json,
                                             "html": list_packages_html,
                                             "compact": print_list_compact})
def list(conan_api: ConanAPI, parser, *args):
    """
    List existing recipes, revisions, or packages in the cache (by default) or the remotes.
    """
    pass
