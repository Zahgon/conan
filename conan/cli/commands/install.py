import os

from conan.api.output import ConanOutput
from conan.cli import make_abs_path
from conan.cli.args import common_graph_args, validate_common_graph_args
from conan.cli.command import conan_command
from conan.cli.formatters.graph import format_graph_json
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_packages, print_graph_basic


@conan_command(group="Consumer", formatters={"json": format_graph_json})
def install(conan_api, parser, *args):
    """
    Install the requirements specified in a recipe (conanfile.py or conanfile.txt).

    It can also be used to install packages without a conanfile, using the
    --requires and --tool-requires arguments.

    If any requirement is not found in the local cache, it will iterate the remotes
    looking for it. When the full dependency graph is computed, and all dependencies
    recipes have been found, it will look for binary packages matching the current settings.
    If no binary package is found for some or several dependencies, it will error,
    unless the '--build' argument is used to build it from source.

    After installation of packages, the generators and deployers will be called.
    """
    pass


def _run_install_command(conan_api, args, cwd, return_install_error=True):
    """
    This method should not be imported as-is, it is internal to the installation process and
    its signature might change without warning.

    Users are however free to copy its code and adapt it to their needs, as an example of
    using the Conan API to perform an installation
    """
    pass
