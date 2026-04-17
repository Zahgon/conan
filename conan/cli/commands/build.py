import os

from conan.api.output import ConanOutput
from conan.cli.command import conan_command
from conan.cli.formatters.graph import format_graph_json
from conan.cli import make_abs_path
from conan.cli.args import add_lockfile_args, add_common_install_arguments, add_reference_args
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_packages, print_graph_basic


@conan_command(group='Creator', formatters={"json": format_graph_json})
def build(conan_api, parser, *args):
    """
    Install dependencies and call the build() method.
    """
    pass
