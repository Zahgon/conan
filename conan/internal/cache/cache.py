import hashlib
import os
import re
import shutil
import uuid
from fnmatch import translate
from typing import List

from conan.internal.cache.conan_reference_layout import RecipeLayout, PackageLayout
# TODO: Random folders are no longer accessible, how to get rid of them asap?
# TODO: We need the workflow to remove existing references.
from conan.internal.cache.db.cache_database import CacheDatabase
from conan.internal.errors import ConanReferenceAlreadyExistsInDB
from conan.errors import ConanException
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.dates import revision_timestamp_now
from conan.internal.util.files import rmdir, renamedir, mkdir


class PkgCache:
    """ Class to represent the recipes and packages storage in disk
    """

    def __init__(self, cache_folder, global_conf):
        # paths
        self._store_folder = global_conf.get("core.cache:storage_path") or \
                             os.path.join(cache_folder, "p")

        try:
            mkdir(self._store_folder)
            db_filename = os.path.join(self._store_folder, 'cache.sqlite3')
            self._base_folder = os.path.abspath(self._store_folder)
            self._db = CacheDatabase(filename=db_filename)
        except Exception as e:
            raise ConanException(f"Couldn't initialize storage in {self._store_folder}: {e}")

    @property
    def store(self):
        pass

    @property
    def temp_folder(self):
        """ temporary folder where Conan puts exports and packages before the final revision
        is computed"""
        pass

    @property
    def builds_folder(self):
        pass

    def _create_path(self, relative_path, remove_contents=True):
        pass

    def _full_path(self, relative_path):
        # This one is used only for rmdir and mkdir operations, not returned to user
        # or stored in DB
        pass

    @staticmethod
    def _short_hash_path(h):
        """:param h: Unicode text to reduce"""
        pass

    @staticmethod
    def _get_path(ref):
        pass

    @staticmethod
    def _get_path_pref(pref):
        pass

    def create_export_recipe_layout(self, ref: RecipeReference):
        """  This is a temporary layout while exporting a new recipe, because the revision is not
        computed until later. The entry is not added to DB, just a temp folder is created

        This temporary export folder will be moved to permanent when revision is computed by the
        assign_rrev() method
        """
        pass

    def create_build_pkg_layout(self, pref: PkgReference):
        # Temporary layout to build a new package, when we don't know the package revision yet
        pass

    def recipe_layout(self, ref: RecipeReference):
        """ the revision must exists, the folder must exist
        The regular graph building will use this method if the revision is defined, like
        when using lockfiles or explicit, or recipe_layout_latest() if not, to do one single DB
        query
        """
        pass

    def recipe_layout_latest(self, ref: RecipeReference):
        """ the revision must be None, the folder must exist
        This method was added so the ConanProxy used to resolve the dependency graph
        avoid doing 2 DB calls when the revision is not defined
        """
        pass

    def get_latest_recipe_revision(self, ref: RecipeReference) -> RecipeReference:
        pass

    def get_recipe_revisions(self, ref: RecipeReference):
        # For listing multiple revisions only
        pass

    def pkg_layout(self, pref: PkgReference):
        """ the revision must exists, the folder must exist
        No longer used by GraphBinariesAnalyzer
        """
        pass

    def pkg_layout_latest(self, pref: PkgReference):
        """
        GraphBinariesAnalyzer will call this method to avoid doing 2 DB calls, previously
        it was using pkg_layout() after a get_latest_package_revision()
        """
        pass

    def create_ref_layout(self, ref: RecipeReference):
        """ called exclusively by:
        - RemoteManager.get_recipe()
        - cache restore
        """
        pass

    def create_pkg_layout(self, pref: PkgReference):
        """ called by:
         - RemoteManager.get_package()
         - cache restore
        """
        pass

    def update_recipe_timestamp(self, ref: RecipeReference):
        """ when the recipe already exists in cache, but we get a new timestamp from a server
        that would affect its order in our cache """
        pass

    def search_recipes(self, pattern=None):
        # Conan references in main storage
        pass

    def exists_prev(self, pref):
        # Used just by download to skip downloads if prev already exists in cache
        pass

    def get_latest_package_revision(self, pref: PkgReference) -> PkgReference:
        # This is no longer needed by the Graph resolution functionality, only by ListAPI
        # its usage in graph resolution has been replaced by a single call to pkg_layout_latest()
        pass

    def get_package_references(self, ref: RecipeReference,
                               only_latest_prev=True) -> List[PkgReference]:
        """Get the latest package references"""
        pass

    def get_package_revisions(self, pref: PkgReference) -> List[PkgReference]:
        pass

    def get_matching_build_id(self, ref, build_id):
        pass

    def remove_recipe_layout(self, layout: RecipeLayout):
        pass

    def remove_package_layout(self, layout: PackageLayout):
        pass

    def remove_build_id(self, pref):
        pass

    def assign_prev(self, layout: PackageLayout):
        pass

    def assign_rrev(self, layout: RecipeLayout):
        """ called at export, once the exported recipe revision has been computed, it
        can register for the first time the new RecipeReference"""
        pass

    def get_recipe_lru(self, ref):
        pass

    def update_recipes_lru(self, refs):
        pass

    def get_package_lru(self, pref):
        pass

    def path_to_ref(self, path):
        pass
