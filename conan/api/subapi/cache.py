import json
import os
import shutil
import tarfile
import tempfile

from conan.api.model import PackagesList
from conan.api.output import ConanOutput
from conan.internal.api.uploader import compress_files, get_compress_level
from conan.internal.cache.cache import PkgCache
from conan.internal.cache.conan_reference_layout import (EXPORT_SRC_FOLDER, EXPORT_FOLDER,
                                                         SRC_FOLDER, METADATA,
                                                         DOWNLOAD_EXPORT_FOLDER)
from conan.internal.cache.home_paths import HomePaths
from conan.internal.cache.integrity_check import IntegrityChecker
from conan.internal.paths import COMPRESSIONS
from conan.internal.rest.download_cache import DownloadCache
from conan.errors import ConanException
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.api.uploader import PackagePreparator
from conan.internal.rest.pkg_sign import PkgSignaturesPlugin
from conan.internal.util.dates import revision_timestamp_now
from conan.internal.util.files import rmdir, mkdir, remove, save


class CacheAPI:
    """ This CacheAPI is used to interact with the packages storage cache

    Note that the Conan packages cache is exclusively **read-only** for user code. Only Conan
    can write or modify the folders and files in the Conan cache. In general, when a method
    returns a folder, it is mostly for debugging purposes and read-only access, but never to
    modify the contents of the cache.
    """

    def __init__(self, conan_api, api_helpers):
        self._conan_api = conan_api
        self._api_helpers = api_helpers

    def export_path(self, ref: RecipeReference):
        """Returns the path of the recipe conanfile and exported files in the Conan cache

        This folder is exclusively for **read-only** access, typically for debugging purposes,
        it is completely forbidden to modify any of its contents.

        :param ref: RecipeReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
        :return: path to the folder, as a string
        :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def recipe_metadata_path(self, ref: RecipeReference):
        """Returns the path of the recipe metadata files in the Conan cache

        Exceptionally, adding or modifying the files within this folder is allowed, as
        the metadata files are not taken into account into the computation of the recipe hash
        (recipe revision).

        :param ref: RecipeReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
        :return: path to the folder, as a string
        :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def export_source_path(self, ref: RecipeReference):
        """Returns the path of the exported sources in the Conan cache

        Note that the exported sources only exist in the cache when the package has been created
        locally or built from source.

        This folder is exclusively for **read-only** access, typically for debugging purposes,
        it is completely forbidden to modify any of its contents.

        :param ref: RecipeReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
        :return: path to the folder, as a string
        :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def source_path(self, ref: RecipeReference):
        """Returns the path of the temporary source folder in the Conan cache

        Note that the source folder only exist in the cache when the package has been created
        locally or built from source.

        This folder is exclusively for **read-only** access, typically for debugging purposes,
        it is completely forbidden to modify any of its contents.

        :param ref: RecipeReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
        :return: path to the folder, as a string
        :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def build_path(self, pref: PkgReference):
        """Returns the path of the temporary build folder in the Conan cache

        Note that the build folder only exist in the cache when the package has been created
        locally or built from source.

        This folder is exclusively for **read-only** access, typically for debugging purposes,
        it is completely forbidden to modify any of its contents.

        :param pref: PkgReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
           Exactly same behavior for the package revision.
        :return: path to the folder, as a string
        :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def package_metadata_path(self, pref: PkgReference):
        """Returns the path of the package metadata folder in the Conan cache

        Exceptionally, adding or modifying the files within this folder is allowed, as
        the metadata files are not taken into account into the computation of the package hash
        (package revision).

       :param pref: PkgReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
           Exactly same behavior for the package revision.
       :return: path to the folder, as a string
       :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def package_path(self, pref: PkgReference):
        """Returns the path of the package folder in the Conan cache

        This folder is exclusively for **read-only** access, typically for debugging purposes,
        it is completely forbidden to modify any of its contents.

        :param pref: PkgReference. If it includes recipe revision, that exact revision will be
           returned, if it doesn't include recipe revision, it will return the latest revision one.
           Exactly same behavior for the package revision.
        :return: path to the folder, as a string
        :raises: ConanExcepcion if the folder doesn't exist
        """
        pass

    def check_integrity(self, package_list, return_pkg_list=False):
        """
        Check if the recipes and packages are corrupted

        :param package_list: PackagesList to check
        :param return_pkg_list: If True, return a PackagesList with corrupted artifacts
        :return: PackagesList with corrupted artifacts if return_pkg_list is True
        :raises: ConanExcepcion if there are corrupted artifacts and return_pkg_list is False
        """
        pass

    def sign(self, package_list):
        """Sign packages with the package signing plugin"""
        pass

    def verify(self, package_list):
        """Verify packages with the package signing plugin"""
        pass

    def clean(self, package_list, source=True, build=True, download=True, temp=True,
              backup_sources=False) -> None:
        """
        Remove non critical folders from the cache, like source, build and download (.tgz store)
        folders.

        :param package_list: the package lists that should be cleaned
        :param source: boolean, remove the "source" folder if True
        :param build: boolean, remove the "build" folder if True
        :param download: boolean, remove the "download (.tgz)" folder if True
        :param temp: boolean, remove the temporary folders
        :param backup_sources: boolean, remove the "source" folder if True
        :return:
        """
        pass

    def save(self, package_list: PackagesList, path, no_source=False) -> None:
        """Create a compressed archive with recipes and packages from the Conan cache that
        can be later restored in another cache.

        Do not manipulate the contents of the resulting archive, as it also contains metadata,
        and modifying the contents would be equivalent to modify the Conan package cache, which
        is forbidden.

        :param package_list: PackagesList containing the recipes and packages to add
           to the compressed archive
        :param path: The archive file to generate. Based on the extension of the file, different
           compression formats can be used (.tgz, .txz and .tzst, the latter only for Python>=3.14).
        :param no_source: If True, the source folders in the cache will not be added to the archive.
        :return:
        """
        pass

    def restore(self, path) -> PackagesList:
        """Restore a compressed archive with recipes and packages previously saved from another
        Conan cache into the currently active Conan cache.

        :param path: The archive file to restore. Based on the extension of the file, different
           compression formats can be used (.tgz, .txz and .tzst, the latter only for Python>=3.14).
        :return: a PackageLists with the recipes and packages that have been restored to the cache
        """
        pass

    def get_backup_sources(self, package_list=None, exclude=True, only_upload=True):
        """Get list of backup source files currently present in the cache,
        either all of them if no argument, or filtered by those belonging to the references
        in the package_list

        :param package_list: a PackagesList object to filter backup files from (The files should
          have been downloaded form any of the references in the package_list)
        :param exclude: if True, exclude the sources that come from URLs present the
          core.sources:exclude_urls global conf
        :param only_upload: if True, only return the files for packages that are set to be uploaded
        :return: A list of files that need to be uploaded
        """
        pass

    def path_to_ref(self, path):
        # This method is explicitly not publicly documented, as mostly a command helper for
        # debugging, it shouldn't be used in any real API usage
        pass


def _resolve_latest_ref(cache, ref):
    pass


def _resolve_latest_pref(cache, pref):
    pass


def _check_folder_existence(ref, folder_name, folder_path):
    pass
