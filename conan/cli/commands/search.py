from collections import OrderedDict

from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern
from conan.cli.command import conan_command
from conan.cli.commands.list import print_list_text, print_list_json
from conan.errors import ConanException


@conan_command(group="Consumer", formatters={"text": print_list_text,
                                             "json": print_list_json})
def search(conan_api: ConanAPI, parser, *args):
    """
    Search for package recipes in all the remotes (by default), or a remote.
    """
    pass
