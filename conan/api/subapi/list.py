import os
from collections import OrderedDict
from typing import Dict

from conan.api.model import PackagesList, MultiPackagesList, ListPattern, Remote
from conan.api.output import ConanOutput, TimedOutput
from conan.internal.api.list.query_parse import filter_package_configs
from conan.internal.model.recipe_ref import ref_matches
from conan.internal.paths import CONANINFO
from conan.internal.errors import NotFoundException
from conan.errors import ConanException
from conan.internal.model.info import load_binary_info
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.dates import timestamp_now
from conan.internal.util.files import load


def _timelimit(expression):
    """ convert an expression like "2d" (2 days) or "3h" (3 hours) to a timestamp in the past
    with respect to current time
    """
    pass


class ListAPI:
    """ Get references from the recipes and packages in the cache or a remote
    """

    def __init__(self, conan_api, api_helpers):
        self._conan_api = conan_api
        self._api_helpers = api_helpers

    def latest_recipe_revision(self, ref: RecipeReference, remote: Remote = None):
        """ For a given recipe reference, return the latest revision of the recipe in the remote,
        or in the local cache if no remote is specified, or ``None`` if the recipe does not exist."""
        pass

    def recipe_revisions(self, ref: RecipeReference, remote: Remote = None):
        """ For a given recipe reference, return all the revisions of the recipe in the remote,
        or in the local cache if no remote is specified"""
        pass

    def latest_package_revision(self, pref: PkgReference, remote=None):
        # TODO: This returns None if the given package_id is not existing. It should probably
        #  raise NotFound, but to keep aligned with the above ``latest_recipe_revision`` which
        #  is used as an "exists" check too in other places, lets respect the None return
        pass

    def package_revisions(self, pref: PkgReference, remote=None):
        pass

    def _packages_configurations(self, ref: RecipeReference,
                                 remote=None) -> Dict[PkgReference, dict]:
        pass

    @staticmethod
    def _filter_packages_configurations(pkg_configurations, query):
        """
        :param pkg_configurations: Dict[PkgReference, PkgConfiguration]
        :param query: str like "os=Windows AND (arch=x86 OR compiler=gcc)"
        :return: Dict[PkgReference, PkgConfiguration]
        """
        pass

    @staticmethod
    def _filter_packages_profile(packages, profile, ref):
        pass

    def select(self, pattern: ListPattern, package_query=None, remote: Remote = None, lru=None,
               profile=None) -> PackagesList:
        """For a given pattern, return a list of recipes and packages matching the provided filters.

        :parameter ListPattern pattern: Search criteria
        :parameter str package_query: When returning packages, expression of the form
            ``"os=Windows AND (arch=x86 OR compiler=gcc)"`` to filter packages by.
            If ``None``, all packages will be returned if requested.
        :parameter Remote remote: Remote to search in,
            if ``None``, it will search in the local cache.
        :parameter str lru: If set, it will filter the results to only include
            packages/binaries that have been used in the last 'lru' time.
            It can be a string like ``"2d"`` (2 days) or ``"3h"`` (3 hours).
        :parameter Profile profile: Profile to filter the packages by settings and options.
        """
        pass

    def explain_missing_binaries(self, ref, conaninfo, remotes):
        """ (Experimental) Explain why a binary is missing in the cache
        """
        pass

    def find_remotes(self, package_list, remotes):
        """
        (Experimental) Find the remotes where the current package lists can be found
        """
        pass

    def outdated(self, deps_graph, remotes):
        # DO NOT USE YET
        # Data structure to store info per library
        pass


class _BinaryDistance:
    def __init__(self, pref, binary, expected, remote=None):
        self.remote = remote
        self.pref = pref
        self.binary_config = binary

        # Settings, special handling for os/arch
        binary_settings = binary.get("settings", {})
        expected_settings = expected.get("settings", {})

        platform = {k: v for k, v in binary_settings.items() if k in ("os", "arch")}
        expected_platform = {k: v for k, v in expected_settings.items() if k in ("os", "arch")}
        self.platform_diff = self._calculate_diff(platform, expected_platform)

        binary_settings = {k: v for k, v in binary_settings.items() if k not in ("os", "arch")}
        expected_settings = {k: v for k, v in expected_settings.items() if k not in ("os", "arch")}
        self.settings_diff = self._calculate_diff(binary_settings, expected_settings)

        self.settings_target_diff = self._calculate_diff(binary, expected, "settings_target")
        self.options_diff = self._calculate_diff(binary, expected, "options")
        self.deps_diff = self._requirement_diff(binary, expected, "requires")
        self.build_requires_diff = self._requirement_diff(binary, expected, "build_requires")
        self.python_requires_diff = self._requirement_diff(binary, expected, "python_requires")
        self.confs_diff = self._calculate_diff(binary,  expected, "conf")

    @staticmethod
    def _requirement_diff(binary_requires, expected_requires, item):
        pass

    @staticmethod
    def _calculate_diff(binary_confs, expected_confs, item=None):
        pass

    def __lt__(self, other):
        return self.distance < other.distance

    def explanation(self):
        pass

    @property
    def distance(self):
        pass

    def serialize(self):
        pass


def _get_cache_packages_binary_info(cache, prefs) -> Dict[PkgReference, dict]:
    """
    param package_layout: Layout for the given reference
    """
    pass


def _search_recipes(api_helpers, query: str, remote=None):
    pass
