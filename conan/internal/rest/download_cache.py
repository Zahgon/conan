import hashlib
import json
import os
from contextlib import contextmanager
from threading import Lock

import fasteners

from conan.errors import ConanException
from conan.internal.util.dates import timestamp_now
from conan.internal.util.files import load, save, remove_if_dirty


class DownloadCache:
    """ The download cache has 3 folders
    - "s": SOURCE_BACKUP for the files.download(internet_url) backup sources feature
    - "c": CONAN_CACHE: for caching Conan packages artifacts
    - "locks": The LOCKS folder containing the file locks for concurrent access to the cache
    """
    _LOCKS = "locks"
    _SOURCE_BACKUP = "s"
    _CONAN_CACHE = "c"

    def __init__(self, path: str):
        self._path: str = path

    def source_path(self, sha256):
        pass

    def cached_path(self, url):
        pass

    _thread_locks = {}  # Needs to be shared among all instances

    @contextmanager
    def lock(self, lock_id):
        pass

    def get_backup_sources_files(self, excluded_urls, package_list=None, only_upload=True):
        """Get list of backup source files currently present in the cache,
        either all of them if no package_list is give, or filtered by those belonging to the references in the package_list

        Will exclude the sources that come from URLs present in excluded_urls

        @param excluded_urls: a list of URLs to exclude backup sources files if they come from any of these URLs
        @param package_list: a PackagesList object to filter backup files from (The files should have been downloaded form any of the references in the package_list)
        @param only_upload: if True, only return the files for packages that are set to be uploaded"""
        pass

    @staticmethod
    def update_backup_sources_json(cached_path, conanfile, urls):
        """ create or update the sha256.json file with the references and new urls used
        """
        pass
