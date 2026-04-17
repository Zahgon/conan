import os
import sqlite3

from conan.api.output import ConanOutput
from conan.internal.cache.db.packages_table import PackagesDBTable
from conan.internal.cache.db.recipes_table import RecipesDBTable
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.model.version import Version


class CacheDatabase:

    def __init__(self, filename):
        version = sqlite3.sqlite_version
        if Version(version) < "3.7.11":
            ConanOutput().error(f"Your sqlite3 '{version} < 3.7.11' version is not supported")
        self._recipes = RecipesDBTable(filename)
        self._packages = PackagesDBTable(filename)
        if not os.path.isfile(filename):
            self._recipes.create_table()
            self._packages.create_table()

    def exists_prev(self, ref):
        pass

    def get_latest_package_reference(self, pref):
        pass

    def get_latest_package_reference_data(self, pref):
        # Used just for PkgCache.pkg_layout_latest()
        # TODO: This can be refactored, unified with get_latest_package_reference()
        pass

    def update_recipe_timestamp(self, ref):
        pass

    def update_package_timestamp(self, pref: PkgReference, path: str, build_id: str):
        pass

    def remove_recipe(self, ref: RecipeReference):
        # Removing the recipe must remove all the package binaries too from DB
        pass

    def remove_package(self, ref: PkgReference):
        # Removing the recipe must remove all the package binaries too from DB
        pass

    def remove_build_id(self, pref):
        pass

    def get_matching_build_id(self, ref, build_id):
        pass

    def get_recipe(self, ref: RecipeReference):
        """ Returns the reference data as a dictionary (or fails) """
        pass

    def get_latest_recipe(self, ref: RecipeReference):
        """ Returns the reference data as a dictionary (or fails) """
        pass

    def get_recipe_revisions_references(self, ref: RecipeReference):
        pass

    def try_get_package(self, ref: PkgReference):
        """ Returns the reference data as a dictionary (or fails) """
        pass

    def create_recipe(self, path, ref: RecipeReference):
        pass

    def create_package(self, path, ref: PkgReference, build_id):
        pass

    def list_references(self, pattern=None):
        """Returns a list of all RecipeReference in the cache, optionally filtering by pattern.
         The references have their revision and timestamp attributes unset"""
        pass

    def get_package_revisions_references(self, pref: PkgReference):
        pass

    def get_package_references(self, ref: RecipeReference, only_latest_prev=True):
        pass

    def path_to_ref(self, path):
        pass
