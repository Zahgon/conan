import os
import shutil

from conan.api.output import ConanOutput
from conan.cli.args import add_lockfile_args, add_common_install_arguments
from conan.cli.command import conan_command, OnceArgument
from conan.cli.commands.export import common_args_export
from conan.cli.formatters.graph import format_graph_json
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_packages, print_graph_basic
from conan.errors import ConanException


@conan_command(group="Creator", formatters={"json": format_graph_json})
def create(conan_api, parser, *args):
    """
    Create a package.
    """
    pass


def _check_tested_reference_matches(deps_graph, tested_ref, out):
    """ Check the test_profile_override_conflict test. If we are testing a build require
    but we specify the build require with a different version in the profile, it has priority,
    it is correct but weird and likely a mistake"""
    pass


def test_package(conan_api, deps_graph, test_conanfile_path):
    pass


def _get_test_conanfile_path(tf, conanfile_path):
    """Searches in the declared test_folder or in the standard "test_package"
    """
    pass
