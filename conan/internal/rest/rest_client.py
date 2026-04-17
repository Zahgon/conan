from conan.internal import REVISIONS
from conan.internal.rest.rest_client_v2 import RestV2Methods
from conan.errors import ConanException

CHECKSUM_DEPLOY = "checksum_deploy"  # capability


class RestApiClient:
    """
        Rest Api Client for handle remote.
    """

    def __init__(self, remote, token, requester, config):
        self._token = token
        self._remote_url = remote.url
        self._requester = requester
        self._verify_ssl = remote.verify_ssl
        self._config = config
        self._remote = remote

    def _capable(self, capability):
        # Caching of capabilities per-remote
        pass

    def _get_api(self):
        pass

    def get_recipe(self, ref, dest_folder, metadata, only_metadata):
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
        # BYPASS capabilities, in case v1/ping is protected
        pass

    def check_credentials(self, force_auth=False):
        pass

    def search(self, pattern=None, ignorecase=True):
        pass

    def search_packages(self, reference, list_only=False):
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
