import binascii
import json
import os
import base64

from conan.internal.api.audit.providers import ConanCenterProvider, PrivateProvider
from conan.errors import ConanException
from conan.internal.api.remotes.encrypt import encode, decode
from conan.internal.model.recipe_ref import RecipeReference
from conan.internal.util.files import save, load

CONAN_CENTER_AUDIT_PROVIDER_NAME = "conancenter"
CYPHER_KEY = "private"


class AuditAPI:
    """
    This class provides the functionality to scan references for vulnerabilities.
    """

    def __init__(self, conan_api):
        self._conan_api = conan_api
        self._home_folder = conan_api.home_folder
        self._providers_path = os.path.join(self._home_folder, "audit_providers.json")
        self._provider_cls = {
            "conan-center-proxy": ConanCenterProvider,
            "private": PrivateProvider,
        }

    @staticmethod
    def scan(deps_graph, provider, context=None):
        """
        Scan a given recipe for vulnerabilities in its dependencies.
        """
        pass

    @staticmethod
    def list(references, provider):
        """
        List the vulnerabilities of the given reference.
        """
        pass

    def get_provider(self, provider_name):
        """
        Get the provider by name.
        """
        pass

    def list_providers(self):
        """
        Get all available providers.
        """
        pass

    def add_provider(self, name, url, provider_type):
        """
        Add a provider.
        """
        pass

    def remove_provider(self, provider_name):
        """
        Remove a provider.
        """
        pass

    def auth_provider(self, provider, token):
        """
        Authenticate a provider.
        """
        pass


def _load_providers(providers_path):
    pass


def _save_providers(providers_path, providers):
    pass
