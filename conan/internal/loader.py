import traceback
from importlib import invalidate_caches, util as imp_util
import inspect
import os
import re
import sys
import types
import uuid
from threading import Lock

import yaml

from pathlib import Path

from conan.api.output import ConanOutput
from conan.tools.cmake import cmake_layout
from conan.tools.google import bazel_layout
from conan.tools.microsoft import vs_layout
from conan.internal.errors import conanfile_exception_formatter, NotFoundException
from conan.errors import ConanException
from conan.internal.model.conan_file import ConanFile
from conan.internal.model.options import Options
from conan.api.model import RecipeReference
from conan.internal.paths import DATA_YML
from conan.internal.model.version_range import validate_conan_version
from conan.internal.util.config_parser import TextINIParse
from conan.internal.util.files import load, chdir, load_user_encoded


class ConanFileLoader:

    def __init__(self, pyreq_loader=None, conanfile_helpers=None):
        self._pyreq_loader = pyreq_loader
        self._cached_conanfile_classes = {}
        self._conanfile_helpers = conanfile_helpers
        invalidate_caches()

    def load_basic(self, conanfile_path, graph_lock=None, display="", remotes=None,
                   update=None, check_update=None):
        """ loads a conanfile basic object without evaluating anything
        """
        pass

    def load_basic_module(self, conanfile_path, graph_lock=None, display="", remotes=None,
                          update=None, check_update=None, tested_python_requires=None):
        """ loads a conanfile basic object without evaluating anything, returns the module too
        """
        pass

    @staticmethod
    def _load_data(conanfile_path):
        pass

    def load_named(self, conanfile_path, name, version, user, channel, graph_lock=None,
                   remotes=None, update=None, check_update=None, tested_python_requires=None):
        """ loads the basic conanfile object and evaluates its name and version
        """
        pass

    def load_export(self, conanfile_path, name, version, user, channel, graph_lock=None,
                    remotes=None):
        """ loads the conanfile and evaluates its name, version, and enforce its existence
        """
        pass

    def load_consumer(self, conanfile_path, name=None, version=None, user=None,
                      channel=None, graph_lock=None,  remotes=None, update=None, check_update=None,
                      tested_python_requires=None):
        """ loads a conanfile.py in user space. Might have name/version or not
        """
        pass

    def load_conanfile(self, conanfile_path, ref, graph_lock=None, remotes=None,
                       update=None, check_update=None):
        """ load a conanfile with a full reference, name, version, user and channel are obtained
        from the reference, not evaluated. Main way to load from the cache
        """
        pass

    def load_conanfile_txt(self, conan_txt_path):
        pass

    @staticmethod
    def _parse_conan_txt(contents, path, display_name):
        pass

    def load_virtual(self, requires=None, tool_requires=None, python_requires=None, graph_lock=None,
                     remotes=None, update=None, check_updates=None):
        # If user don't specify namespace in options, assume that it is
        # for the reference (keep compatibility)
        pass


def _parse_module(conanfile_module, module_id):
    """ Parses a python in-memory module, to extract the classes, mainly the main
    class defining the Recipe, but also process possible existing generators
    @param conanfile_module: the module to be processed
    @return: the main ConanFile class from the module
    """
    pass


_load_python_lock = Lock()  # Loading our Python files is not thread-safe (modifies sys)


def _parse_conanfile(conanfile_path):
    pass


def load_python_file(conan_file_path):
    """ From a given path, obtain the in memory python import module
    """
    pass


def _load_python_file(conan_file_path):
    """ From a given path, obtain the in memory python import module
    """
    pass


def _get_required_conan_version_without_loading(conan_file_path):
    # First, try to detect the required_conan_version in "text" mode
    # https://github.com/conan-io/conan/issues/11239
    pass


class ConanFileTextLoader:
    """Parse a conanfile.txt file"""

    def __init__(self, input_text):
        # Prefer composition over inheritance, the __getattr__ was breaking things
        self._config_parser = TextINIParse(input_text,  ["requires", "generators", "options",
                                                         "imports", "tool_requires", "test_requires",
                                                         "layout"],
                                           strip_comments=True)

    @property
    def layout(self):
        """returns the declared layout"""
        pass

    @property
    def requirements(self):
        """returns a list of requires
        EX:  "OpenCV/2.4.10@phil/stable"
        """
        pass

    @property
    def tool_requirements(self):
        """returns a list of tool_requires
        EX:  "OpenCV/2.4.10@phil/stable"
        """
        pass

    @property
    def test_requirements(self):
        """returns a list of test_requires
        EX:  "gtest/2.4.10@phil/stable"
        """
        pass

    @property
    def options(self):
        pass

    @property
    def generators(self):
        pass
