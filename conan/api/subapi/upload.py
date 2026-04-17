import os
import time
from multiprocessing.pool import ThreadPool
from typing import List

from conan.api.model import PackagesList, Remote
from conan.api.output import ConanOutput
from conan.internal.api.upload import add_urls
from conan.internal.api.uploader import PackagePreparator, UploadExecutor, UploadUpstreamChecker
from conan.internal.rest.pkg_sign import PkgSignaturesPlugin
from conan.internal.rest.file_uploader import FileUploader
from conan.internal.errors import AuthenticationException, ForbiddenException
from conan.errors import ConanException


class UploadAPI:
    """ This API is used to upload recipes and packages to a remote server."""

    def __init__(self, conan_api, api_helpers):
        self._conan_api = conan_api
        self._api_helpers = api_helpers

    def check_upstream(self, package_list: PackagesList, remote: Remote,
                       enabled_remotes: List[Remote], force=False):
        """ Checks ``remote`` for the existence of the recipes and packages in ``package_list``.
        Items that are not present in the remote will add an ``upload`` key to the entry
        with the value ``True``.

        If the recipe has an upload policy of ``skip``, it will be discarded from the upload list.

        :parameter package_list: A ``PackagesList`` object with the recipes and packages to check.
        :parameter remote: Remote to check.
        :parameter enabled_remotes: List of enabled remotes. This is used to possibly load
            python_requires from the listed recipes if necessary.
        :parameter force: If ``True``, it will skip the check and mark that all items need to be
            uploaded. A ``force_upload`` key will be added to the entries that will be uploaded.
        """
        pass

    def prepare(self, package_list: PackagesList, enabled_remotes: List[Remote],
                metadata: List[str] = None):
        """Compress the recipes and packages and fill the upload_data objects
        with the complete information. It doesn't perform the upload nor checks upstream to see
        if the recipe is still there

        :param package_list: A PackagesList object with the recipes and packages to upload.
        :param enabled_remotes: A list of remotes that are enabled in the client.
            Recipe sources will attempt to be fetched from these remotes.
        :param metadata: A list of patterns of metadata that should be uploaded.
            Default ``None`` means all metadata will be uploaded together with the package artifacts.
            If metadata contains an empty string (``""``),
            it means that no metadata files should be uploaded."""
        pass

    def _upload(self, package_list, remote):
        pass

    def upload_full(self, package_list: PackagesList, remote: Remote, enabled_remotes: List[Remote],
                    check_integrity=False, force=False, metadata: List[str] = None, dry_run=False):
        """ Does the whole process of uploading, including the possibility of parallelizing
        per recipe based on the ``core.upload:parallel`` conf.

        The steps that this method performs are:
            - calls ``conan_api.cache.check_integrity`` to ensure the packages are not corrupted
            - checks the upload policy of the recipes
                - (if it is ``"skip"``, it will not upload the binaries, but will still upload
                  the metadata)
            - checks which revisions already exist in the server so that it can skip the upload
            - prepares the artifacts to upload (compresses the conan_package.tgz)
            - executes the actual upload
            - uploads associated sources backups if any

        :param package_list: A PackagesList object with the recipes and packages to upload.
        :param remote: The remote to upload the packages to.
        :param enabled_remotes: A list of remotes that are enabled in the client.
            Recipe sources will attempt to be fetched from these remotes,
            and to possibly load python_requires from the listed recipes if necessary.
        :param check_integrity: If ``True``, it will check the integrity of the cache packages
            before uploading them. This is useful to ensure that the packages are not corrupted.
        :param force: If ``True``, it will force the upload of the recipes and packages,
            even if they already exist in the remote. Note that this might update the timestamps
        :param metadata: A list of patterns of metadata that should be uploaded.
            Default ``None`` means all metadata will be uploaded together with the package artifacts.
            If metadata contains an empty string (``""``),
            it means that no metadata files should be uploaded.
        :param dry_run: If ``True``, it will not perform the actual upload,
            but will still prepare the artifacts and check the upstream.
        """
        pass

    def upload_backup_sources(self, files: List) -> None:
        """
        Upload to the server the backup sources files, that have been typically gathered by
        CacheAPI.get_backup_sources()

        :param files: The list of files that must be uploaded
        """
        pass
