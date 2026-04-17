from conan.api.output import ConanOutput
from conan.internal.graph.proxy import should_update_reference
from conan.errors import ConanException
from conan.api.model import RecipeReference
from conan.internal.model.version_range import VersionRange


class RangeResolver:

    def __init__(self, cache, remote_manager, global_conf, editable_packages):
        self._cache = cache
        self._editable_packages = editable_packages
        self._remote_manager = remote_manager
        self._cached_cache = {}  # Cache caching of search result, so invariant wrt installations
        self._cached_remote_found = {}  # dict {ref (pkg/*): {remote_name: results (pkg/1, pkg/2)}}
        self.resolved_ranges = {}
        self._resolve_prereleases = global_conf.get('core.version_ranges:resolve_prereleases')

    def resolve(self, require, base_conanref, remotes, update):
        pass

    def _resolve_local(self, search_ref, version_range):
        pass

    def _search_remote_recipes(self, remote, search_ref):
        pass

    def _resolve_remote(self, search_ref, version_range, remotes, update):
        pass

    @staticmethod
    def _resolve_version(version_range, refs_found, resolve_prereleases):
        pass
