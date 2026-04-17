import os

from conan.cli.command import conan_command


@conan_command(group="Creator")
def new(conan_api, parser, *args):
    """
    Create a new example recipe and source files from a template.
    """
    pass
