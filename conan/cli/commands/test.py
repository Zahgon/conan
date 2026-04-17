import os

from conan.api.output import ConanOutput
from conan.cli.command import conan_command, OnceArgument
from conan.cli.commands.create import test_package, _check_tested_reference_matches
from conan.cli.args import add_lockfile_args, add_common_install_arguments
from conan.cli.formatters.graph import format_graph_json
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_basic, print_graph_packages
from conan.api.model import RecipeReference


@conan_command(group="Creator", formatters={"json": format_graph_json})
def test(conan_api, parser, *args):
    """
    Test a package from a test_package folder.
    """
    pass


def run_test(conan_api, path, ref, profile_host, profile_build, remotes, lockfile, update,
             build_modes, tested_python_requires=None, build_modes_test=None, tested_graph=None):
    pass
