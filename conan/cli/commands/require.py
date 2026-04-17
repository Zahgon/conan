import os
import re

from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, RecipeReference
from conan.api.output import ConanOutput
from conan.cli.command import conan_command, conan_subcommand
from conan.errors import ConanException
from conan.internal.util.files import save, load


@conan_subcommand()
def require_remove(conan_api, parser, subparser, *args):
    """
    Removes a requirement from your local conanfile.
    """
    pass


@conan_subcommand()
def require_add(conan_api, parser, subparser, *args):
    """
    Add a new requirement to your local conanfile as a version range.
    By default, it will look for the requirement versions remotely.
    """
    pass


@conan_command(group="Consumer")
def require(conan_api: ConanAPI, parser, *args):
    """
    Adds/removes requirements to/from your local conanfile.
    """
