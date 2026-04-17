import os

from conan.cli.command import conan_command
from conan.cli.args import add_reference_args


@conan_command(group="Creator")
def source(conan_api, parser, *args):
    """
    Call the source() method.
    """
    pass
