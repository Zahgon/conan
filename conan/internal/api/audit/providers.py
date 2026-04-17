import textwrap
from urllib.parse import urljoin
from conan.api.output import Color, ConanOutput
from conan.errors import ConanException


def _build_headers(token):
    pass


class ConanCenterProvider:
    def __init__(self, conan_api, name, provider_data):
        self.name = name
        self.url = provider_data["url"]
        self.type = provider_data["type"]
        self._token = provider_data.get("token")
        self._session = conan_api._api_helpers.requester  # noqa
        self._query_url = urljoin(self.url, "api/v1/query")

    def get_cves(self, refs):
        pass


class PrivateProvider:
    def __init__(self, conan_api, name, provider_data):
        self.name = name
        self.url = provider_data["url"]
        self.type = provider_data["type"]
        self._token = provider_data.get("token")
        self._session = conan_api._api_helpers.requester  # noqa
        self._query_url = urljoin(self.url, "catalog/api/v0/public/graphql")

    def get_cves(self, refs):
        pass

    @staticmethod
    def _build_query(ref):
        pass

    @staticmethod
    def _parse_error(errors, ref):
        """This function removes the errors array that comes from the catalog and returns a
        more user-friendly message if we know how to parse it, or a generic one if we don't
        find such one"""
        pass

    def _get(self, ref):
        pass
