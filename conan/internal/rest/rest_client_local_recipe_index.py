import os
import sys
import textwrap
from fnmatch import fnmatch
from io import StringIO

import yaml

from conan.api.model import LOCAL_RECIPES_INDEX
from conan.api.output import ConanOutput
from conan.internal.cache.home_paths import HomePaths
from conan.internal.api.export import cmd_export
from conan.internal.hook_manager import HookManager
from conan.internal.loader import ConanFileLoader
from conan.internal.errors import ConanReferenceDoesNotExistInDB, RecipeNotFoundException, \
    PackageNotFoundException
from conan.errors import ConanException
from conan.internal.model.conf import ConfDefinition
from conan.api.model import RecipeReference
from conan.internal.util.files import load, save, rmdir, copytree_compat


def add_local_recipes_index_remote(home_folder, remote):
    pass


def remove_local_recipes_index_remote(home_folder, remote):
    pass


class RestApiClientLocalRecipesIndex:
    """
    Implements the RestAPI but instead of over HTTP for a remote server, using just
    a local folder assuming the conan-center-index repo layout
    """

    def __init__(self, remote, home_folder):
        self._remote = remote
        local_recipes_index_path = HomePaths(home_folder).local_recipes_index_path
        local_recipes_index_path = os.path.join(local_recipes_index_path, remote.name, ".conan")
        repo_folder = self._remote.url

        from conan.internal.conan_app import LocalRecipesIndexApp
        self._app = LocalRecipesIndexApp(local_recipes_index_path)
        self._hook_manager = HookManager(HomePaths(local_recipes_index_path).hooks_path)
        self._layout = _LocalRecipesIndexLayout(repo_folder)

    def call_method(self, method_name, *args, **kwargs):
        pass

    def get_recipe(self, ref, dest_folder):
        pass

    def get_recipe_sources(self, ref, dest_folder):
        pass

    def get_package(self, pref, dest_folder, metadata, only_metadata):
        pass

    def upload_recipe(self, ref, files_to_upload):
        pass

    def upload_package(self, pref, files_to_upload):
        pass

    def authenticate(self, user, password):
        pass

    def check_credentials(self, force_auth=False):
        pass

    def search(self, pattern=None):
        pass

    def search_packages(self, reference, _=False):
        pass

    def remove_recipe(self, ref):
        pass

    def remove_all_packages(self, ref):
        pass

    def remove_packages(self, prefs):
        pass

    def get_recipe_revisions_references(self, ref):
        pass

    def get_package_revisions_references(self, pref):
        pass

    def get_latest_recipe_reference(self, ref):
        pass

    def get_latest_package_reference(self, pref, headers):
        pass

    def get_recipe_revision_reference(self, ref):
        pass

    def get_package_revision_reference(self, pref):
        pass

    # Helper methods to implement the interface
    def _export_recipe(self, ref):
        pass

    @staticmethod
    def _copy_files(source_folder, dest_folder):
        pass


class _LocalRecipesIndexLayout:

    def __init__(self, base_folder):
        self._base_folder = base_folder

    def _get_base_folder(self, recipe_name):
        pass

    @staticmethod
    def _load_config_yml(folder):
        pass

    def get_recipes_references(self, pattern):
        pass

    def get_recipe_folder(self, ref):
        pass
