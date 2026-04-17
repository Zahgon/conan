import os
import shutil
import sys

from collections import namedtuple
from typing import List

from requests.exceptions import ConnectionError

from conan.api.model import LOCAL_RECIPES_INDEX
from conan.internal.paths import CONANINFO, CONAN_MANIFEST, PACKAGE_FILE_NAME, EXPORT_FILE_NAME
from conan.internal.rest.rest_client_local_recipe_index import RestApiClientLocalRecipesIndex
from conan.api.model import Remote
from conan.api.output import ConanOutput
from conan.internal.cache.conan_reference_layout import METADATA
from conan.internal.rest.pkg_sign import PkgSignaturesPlugin
from conan.internal.errors import ConanConnectionError, NotFoundException, PackageNotFoundException
from conan.errors import ConanException
from conan.internal.model.info import load_binary_info
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.files import rmdir, human_size
from conan.internal.util.files import mkdir, tar_extract


class RemoteManager:
    """ Will handle the remotes to get recipes, packages etc """

    _ErrorMsg = namedtuple("ErrorMsg", ["message"])

    def __init__(self, cache, auth_manager, home_folder):
        self._cache = cache
        self._auth_manager = auth_manager
        self._signer = PkgSignaturesPlugin(cache, home_folder)
        self._home_folder = home_folder

    def _local_folder_remote(self, remote):
        pass

    def check_credentials(self, remote, force_auth=False):
        pass

    def upload_recipe(self, ref, files_to_upload, remote):
        pass

    def upload_package(self, pref, files_to_upload, remote):
        pass

    def get_recipe(self, ref, remote, metadata=None):
        pass

    def _download_recipe(self, layout, ref, remote, metadata):
        pass

    def get_recipe_metadata(self, recipe_layout, ref, remote, metadata):
        """
        Get only the metadata for a locally existing recipe in Cache
        """
        pass

    def get_recipe_sources(self, ref, layout, remote):
        pass

    def get_package(self, pref, remote, metadata=None):
        pass

    def get_package_metadata(self, pref, remote, metadata):
        """
        only download the metadata, not the packge itself
        """
        pass

    def _get_package(self, layout, pref, remote, scoped_output, metadata):
        pass

    def search_recipes(self, remote, pattern):
        # Used by ListAPI to "conan list *" recipes, and by RangeResolver to resolve version-ranges
        pass

    def search_packages(self, remote, ref, list_only=False):
        # Used only by ListAPI to list the different package_ids for a reference
        pass

    def remove_recipe(self, ref, remote):
        pass

    def remove_packages(self, prefs, remote):
        pass

    def remove_all_packages(self, ref, remote):
        pass

    def authenticate(self, remote, name, password):
        pass

    def get_recipe_revisions(self, ref: RecipeReference, remote: Remote) -> List[RecipeReference]:
        # Used by ListAPI to list recipe revisions for a ref without revision
        # and by ConanProxy resolving legacy_update Conan 1 logic
        pass

    def get_recipe_revision(self, ref: RecipeReference, remote: Remote) -> RecipeReference:
        # Used by UploadUpstreamChecker to see if the revision exist in the server
        # Used by Download, to get timestamp from server and respect it
        # Used by ConanProxy to confirm existence of specific revision
        pass

    def get_latest_recipe_revision(self, ref: RecipeReference, remote: Remote) -> RecipeReference:
        # Used by ListAPI to retrieve the latest revision
        # Used by ConanProxy to resolve to the latest revision
        pass

    def get_package_revisions(self, pref: PkgReference, remote: Remote) -> List[PkgReference]:
        # Used by ListAPI to retrieve multiple package revisions
        pass

    def get_package_revision(self, pref: PkgReference, remote: Remote) -> PkgReference:
        # Used by UploadUpstreamChecker to see if the revision exist in the server
        # Used by Download, to get timestamp from server and respect it
        pass

    def get_latest_package_revision(self, pref: PkgReference, remote: Remote,
                                    info=None) -> PkgReference:
        # Used by List to resolve the latest package revision
        # Used by GraphBinariesAnalyzer to resolve to latest package revision
        pass

    def _call_remote(self, remote, method, *args, **kwargs):
        pass


def uncompress_file(src_path, dest_folder, scope=None):
    pass
