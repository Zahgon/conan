import json
import os
from shutil import which

from conan.tools.build import cmd_args_to_string
from conan.errors import ConanException


def vs_installation_path(version):
    pass


def vs_detect_update(version):
    pass


def _vs_installation_path(version):
    # TODO: Preference hardcoded, [conf] must be defined
    pass


def vswhere(all_=False, prerelease=True, products=None, requires=None, version="", latest=False,
            legacy=False, property_="", nologo=True):

    # 'version' option only works if Visual Studio 2017 is installed:
    # https://github.com/Microsoft/vswhere/issues/91

    pass
