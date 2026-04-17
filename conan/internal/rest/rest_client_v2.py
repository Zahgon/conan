import copy
import fnmatch
import hashlib
import json
import os
from threading import Thread

from requests.auth import AuthBase, HTTPBasicAuth
from uuid import getnode as get_mac

from conan.api.output import ConanOutput
from conan.internal.paths import EXPORT_SOURCES_FILE_NAME, CONANINFO, CONAN_MANIFEST, \
    EXPORT_FILE_NAME, PACKAGE_FILE_NAME
from conan.internal.rest.caching_file_downloader import ConanInternalCacheDownloader
from conan.internal.rest import response_to_str
from conan.internal.rest.client_routes import ClientV2Router
from conan.internal.rest.file_uploader import FileUploader
from conan.internal.errors import AuthenticationException, ForbiddenException, NotFoundException, \
    RecipeNotFoundException, PackageNotFoundException, EXCEPTION_CODE_MAPPING
from conan.errors import ConanException
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.dates import from_iso8601_to_timestamp


# TODO: We might want to replace this raw Thread for a ThreadPool, to align with other code usages
class ExceptionThread(Thread):
    def run(self):
        pass

    def join(self, timeout=None):
        pass

    def raise_errors(self):
        pass


class JWTAuth(AuthBase):
    """Attaches JWT Authentication to the given Request object."""

    def __init__(self, token):
        self.bearer = "Bearer %s" % str(token) if token else None

    def __call__(self, request):
        if self.bearer:
            request.headers['Authorization'] = self.bearer
        return request


def _raise_exception_from_error(error_code, text):
    pass


def _get_mac_digest():  # To avoid re-hashing all the time the same mac
    pass


class RestV2Methods:

    def __init__(self, remote_url, token, requester, config, verify_ssl, checksum_deploy=False):
        self.remote_url = remote_url
        self.custom_headers = {'X-Client-Anonymous-Id': _get_mac_digest()}
        self.requester = requester
        self._config = config
        self.verify_ssl = verify_ssl
        self._checksum_deploy = checksum_deploy
        self.router = ClientV2Router(self.remote_url.rstrip("/"))
        self.auth = JWTAuth(token)

    @staticmethod
    def _check_error_response(ret):
        pass

    def authenticate(self, user, password):
        """Sends user + password to get:
          - A plain response with a regular token (not supported refresh in the remote) and None
        """
        pass

    def check_credentials(self, force_auth=False):
        """If token is not valid will raise AuthenticationException.
        User will be asked for new user/pass"""
        pass

    def server_capabilities(self):
        """Get information about the server: status, version, type and capabilities"""
        pass

    def _get_json(self, url, headers=None):
        pass

    def upload_recipe(self, ref, files_to_upload):
        pass

    def upload_package(self, pref, files_to_upload):
        pass

    def search(self, pattern=None, ignorecase=True):
        """
        the_files: dict with relative_path: content
        """
        pass

    def search_packages(self, ref, list_only):
        """Client is filtering by the query"""
        pass

    def _get_file_list_json(self, url):
        pass

    def get_recipe(self, ref, dest_folder, metadata, only_metadata):
        pass

    def get_recipe_sources(self, ref, dest_folder):
        # If revision not specified, check latest
        pass

    @staticmethod
    def _find_compressed_file(ref, server_files, artifact, exists=False):
        pass

    def get_package(self, pref, dest_folder, metadata, only_metadata):
        pass

    def _upload_files(self, files, urls, ref):
        pass

    def _download_and_save_files(self, urls, dest_folder, files, parallel=False, scope=None,
                                 metadata=False):
        # Take advantage of filenames ordering, so that conan_package.tgz and conan_export.tgz
        # can be < conanfile, conaninfo, and sent always the last, so smaller files go first
        pass

    def remove_all_packages(self, ref):
        """ Remove all packages from the specified reference"""
        pass

    def remove_packages(self, prefs):
        pass

    def remove_recipe(self, ref):
        """ Remove a recipe and packages """
        pass

    def get_recipe_revision_reference(self, ref):
        # FIXME: implement this new endpoint in the remotes?
        pass

    def get_package_revision_reference(self, pref):
        # FIXME: implement this endpoint in the remotes?
        pass

    def get_recipe_revisions_references(self, ref):
        pass

    def get_latest_recipe_reference(self, ref):
        pass

    def get_package_revisions_references(self, pref):
        pass

    def get_latest_package_reference(self, pref: PkgReference, headers):
        pass
