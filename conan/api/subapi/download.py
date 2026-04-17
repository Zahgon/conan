import time
from multiprocessing.pool import ThreadPool
from typing import Optional, List

from conan.api.model import Remote, PackagesList
from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.api.model import PkgReference
from conan.api.model import RecipeReference


class DownloadAPI:
    """ This API is used to download recipes and packages from a remote server."""

    def __init__(self, conan_api, api_helpers):
        self._conan_api = conan_api
        self._api_helpers = api_helpers

    def recipe(self, ref: RecipeReference, remote: Remote, metadata: Optional[List[str]] = None):
        """Download the recipe specified in the ref from the remote.
        If the recipe is already in the cache it will be skipped,
        but the specified metadata will be downloaded."""
        pass

    def package(self, pref: PkgReference, remote: Remote, metadata: Optional[List[str]] = None):
        """Download the package specified in the pref from the remote.
        The recipe for this package binary must already exist in the cache.
        If the package is already in the cache it will be skipped,
        but the specified metadata will be downloaded."""
        pass

    def download_full(self, package_list: PackagesList, remote: Remote,
                      metadata: Optional[List[str]] = None):
        """Download the recipes and packages specified in the ``package_list`` from the remote,
        parallelized based on ``core.download:parallel``"""
        pass
