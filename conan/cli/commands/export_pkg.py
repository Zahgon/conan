import os

from conan.api.output import ConanOutput
from conan.cli import make_abs_path
from conan.cli.args import add_lockfile_args, add_profiles_args, add_reference_args
from conan.cli.command import conan_command, OnceArgument
from conan.cli.commands.create import _get_test_conanfile_path
from conan.cli.formatters.graph import format_graph_json
from conan.errors import ConanException


@conan_command(group="Creator", formatters={"json": format_graph_json})
def export_pkg(conan_api, parser, *args):
    """
    Create a package directly from pre-compiled binaries.
    """
    pass
