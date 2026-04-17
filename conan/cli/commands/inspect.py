import os

from conan.api.output import cli_out_write
from conan.cli.command import conan_command, OnceArgument
from conan.cli.formatters import default_json_formatter


def inspect_text_formatter(data):
    pass


@conan_command(group="Consumer", formatters={"text": inspect_text_formatter,
                                             "json": default_json_formatter})
def inspect(conan_api, parser, *args):
    """
    Inspect a conanfile.py to return its public fields.
    """
    pass
