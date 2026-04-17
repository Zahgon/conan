import os
import tempfile

from conan.api.output import ConanOutput, LEVEL_STATUS, Color, LEVEL_ERROR, LEVEL_QUIET
from conan.cli.args import common_graph_args, validate_common_graph_args
from conan.cli.command import conan_command
from conan.cli.commands.install import _run_install_command
from conan.errors import ConanException


@conan_command(group="Consumer")
def run(conan_api, parser, *args):
    """
    (Experimental) Run a command given a set of requirements from a recipe or from command line.
    """
    pass
