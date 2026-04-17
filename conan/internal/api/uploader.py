import fnmatch
import gzip
import os
import shutil
import sys
import tarfile
import time

from conan.api.output import ConanOutput
from conan.internal.source import retrieve_exports_sources
from conan.internal.errors import NotFoundException
from conan.errors import ConanException
from conan.internal.paths import CONAN_MANIFEST, CONANFILE, CONANINFO, COMPRESSIONS, \
    EXPORT_SOURCES_FILE_NAME, EXPORT_FILE_NAME, PACKAGE_FILE_NAME
from conan.internal.util.files import (clean_dirty, is_dirty, gather_files,
                                       set_dirty_context_manager, mkdir, human_size)

UPLOAD_POLICY_FORCE = "force-upload"
UPLOAD_POLICY_SKIP = "skip-upload"


class UploadUpstreamChecker:
    """ decides if something needs to be uploaded or force-uploaded checking if that exact
    revision already exists in the remote server, or if the --force parameter is forcing the upload
    This is completely irrespective of the actual package contents, it only uses the local
    computed revision and the remote one
    """
    def __init__(self, remote_manager):
        self._remote_manager = remote_manager

    def check(self, package_list, remote, force):
        pass

    def _check_upstream_recipe(self, ref, ref_bundle, remote, force):
        pass

    def _check_upstream_package(self, pref, prev_bundle, remote, force):
        pass


def get_compress_level(compressformat, global_conf):
    pass


class PackagePreparator:
    def __init__(self, loader, cache, remote_manager, global_conf):
        self._loader = loader
        self._remote_manager = remote_manager
        self._cache = cache
        self._global_conf = global_conf
        compressformat = self._global_conf.get("core.upload:compression_format", default="gz",
                                               choices=COMPRESSIONS)
        compresslevel = get_compress_level(compressformat, global_conf)
        self._compressformat = compressformat
        self._compresslevel = compresslevel

    def prepare(self, pkg_list, enabled_remotes, metadata, force=False):
        pass

    def _prepare_recipe(self, recipe_layout, ref, ref_bundle, conanfile, remotes):
        """ do a bunch of things that are necessary before actually executing the upload:
        - retrieve exports_sources to complete the recipe if necessary
        - compress the artifacts in conan_export.tgz and conan_export_sources.tgz
        """
        pass

    def _compress_recipe_files(self, layout, ref):
        pass

    def _prepare_package(self, pref, prev_bundle, metadata, force=False):
        pass

    def _compressed_file(self, filename, files, download_folder, ref):
        pass

    def _compress_package_files(self, layout, pref):
        pass


class UploadExecutor:
    """ does the actual file transfer to the remote. The files to be uploaded have already
    been computed and are passed in the ``upload_data`` parameter, so this executor is also
    agnostic about which files are transferred
    """
    def __init__(self, remote_manager):
        self._remote_manager = remote_manager

    def upload(self, upload_data, remote):
        pass

    def upload_recipe(self, ref, bundle, remote):
        pass

    def upload_package(self, pref, prev_bundle, remote):
        pass


def gzopen_without_timestamps(name, fileobj, compresslevel=None):
    """ !! Method overrided by laso to pass mtime=0 (!=None) to avoid time.time() was
        setted in Gzip file causing md5 to change. Not possible using the
        previous tarfile open because arguments are not passed to GzipFile constructor
    """
    pass


def compress_files(files, name, dest_dir, compresslevel=None, scope=None, recursive=False):
    pass


def _total_size(cache_files):
    pass


def _metadata_files(folder, metadata):
    pass
