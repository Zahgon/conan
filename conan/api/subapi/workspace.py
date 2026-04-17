import inspect
import os
import shutil
import textwrap
from pathlib import Path

from conan import ConanFile
from conan.api.model import RecipeReference
from conan.api.output import ConanOutput
from conan.cli import make_abs_path
from conan.cli.printers.graph import print_graph_basic, print_graph_packages
from conan.errors import ConanException
from conan.internal.errors import conanfile_exception_formatter
from conan.internal.graph.install_graph import ProfileArgs
from conan.internal.methods import auto_language, auto_shared_fpic_config_options, \
    auto_shared_fpic_configure
from conan.internal.model.options import Options
from conan.internal.model.workspace import Workspace, WORKSPACE_YML, WORKSPACE_PY, WORKSPACE_FOLDER
from conan.tools.scm import Git
from conan.internal.graph.graph import (RECIPE_EDITABLE, DepsGraph, CONTEXT_HOST, RECIPE_VIRTUAL,
                                        Node, RECIPE_CONSUMER)
from conan.internal.graph.graph import TransitiveRequirement
from conan.internal.graph.profile_node_definer import consumer_definer, initialize_conanfile_profile
from conan.internal.loader import load_python_file
from conan.internal.source import retrieve_exports_sources
from conan.internal.util.files import merge_directories, save


def _find_ws_folder():
    pass


def _load_workspace(ws_folder, conan_api):
    """ loads a conanfile basic object without evaluating anything, returns the module too
    """
    pass


def _parse_module(conanfile_module, module_id):
    pass


class WorkspaceAPI:
    TEST_ENABLED = False

    def __init__(self, conan_api):
        self._enabled = True
        self._conan_api = conan_api
        self._folder = _find_ws_folder()
        if self._folder:
            ConanOutput().warning(f"Workspace found: {self._folder}")
            if (WorkspaceAPI.TEST_ENABLED or os.getenv("CONAN_WORKSPACE_ENABLE")) != "will_break_next":
                ConanOutput().warning("Workspace ignored as CONAN_WORKSPACE_ENABLE is not set")
                self._folder = None
            else:
                ConanOutput().warning(f"Workspace is a dev-only feature, exclusively for testing")
                self._ws = _load_workspace(self._folder, conan_api)  # Error if not loading

    def enable(self, value):
        pass

    def name(self):
        pass

    def folder(self):
        """
        @return: the current workspace folder where the conanws.yml or conanws.py is located
        """
        pass

    def packages(self):
        """
        @return: Returns {RecipeReference: {"path": full abs-path, "output_folder": abs-path}}
        """
        pass

    def open(self, ref, remotes, cwd=None):
        pass

    def _check_ws(self):
        pass

    def add(self, path, name=None, version=None, user=None, channel=None, cwd=None,
            output_folder=None, remotes=None):
        """
        Add a new editable package to the current workspace (the current workspace must exist)
        @param path: The path to the folder containing the conanfile.py that defines the package
        @param name: (optional) The name of the package to be added if not defined in recipe
        @param version:
        @param user:
        @param channel:
        @param cwd:
        @param output_folder:
        @param remotes:
        @return: The reference of the added package
        """
        pass

    def complete(self, profile_host, profile_build, lockfile, remotes, update):
        pass

    @staticmethod
    def init(path):
        pass

    def remove(self, path):
        pass

    def clean(self):
        pass

    def info(self):
        pass

    @staticmethod
    def _init_options(conanfile, options):
        pass

    def super_build_graph(self, deps_graph, profile_host, profile_build):
        pass

    @staticmethod
    def _check_graph(graph):
        pass

    def export(self, lockfile=None, remotes=None):
        pass

    def select_packages(self, packages):
        pass

    def build_order(self, packages, profile_host, profile_build, build_mode, lockfile, remotes,
                    profile_args, update=False):
        pass
