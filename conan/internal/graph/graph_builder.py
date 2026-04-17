import os
from collections import deque

from conan.internal.cache.conan_reference_layout import BasicLayout
from conan.internal.methods import run_configure_method
from conan.internal.model.recipe_ref import ref_matches
from conan.internal.graph.graph import DepsGraph, Node, CONTEXT_HOST, \
    CONTEXT_BUILD, TransitiveRequirement, RECIPE_VIRTUAL, RECIPE_EDITABLE, RECIPE_CONSUMER
from conan.internal.graph.graph import RECIPE_PLATFORM
from conan.internal.graph.graph_error import (GraphLoopError, GraphConflictError, GraphMissingError,
                                              GraphError)
from conan.internal.graph.profile_node_definer import initialize_conanfile_profile
from conan.internal.graph.provides import check_graph_provides
from conan.errors import ConanException
from conan.internal.model.conan_file import ConanFile
from conan.internal.model.options import Options, _PackageOptions
from conan.internal.model.pkg_type import PackageType
from conan.api.model import RecipeReference
from conan.internal.model.requires import Requirement
from conan.internal.model.version_range import VersionRange


class DepsGraphBuilder:
    ALLOW_ALIAS = False

    def __init__(self, proxy, loader, resolver, cache, remotes, update, check_update, global_conf):
        self._proxy = proxy
        self._loader = loader
        self._resolver = resolver
        self._cache = cache
        self._remotes = remotes  # TODO: pass as arg to load_graph()
        self._update = update
        self._check_update = check_update
        self._resolve_prereleases = global_conf.get('core.version_ranges:resolve_prereleases')

    def load_graph(self, root_node, profile_host, profile_build, graph_lock=None):
        pass

    def _expand_require(self, require, node, graph, profile_host, profile_build, graph_lock):
        # Handle a requirement of a node. There are 2 possibilities
        #    node -(require)-> new_node (creates a new node in the graph)
        #    node -(require)-> previous (creates a diamond with a previously existing node)
        # TODO: allow bootstrapping, use references instead of names
        # print("  Expanding require ", node, "->", require)
        pass

    def _save_options_conflicts(self, node, require, prev_node, graph):
        """ Store the discrepancies of options when closing a diamond, to later report
        them. This list is not exhaustive, only the diamond vertix, not other transitives
        """
        pass

    @staticmethod
    def _conflicting_version(require, node,
                             prev_require, prev_node, prev_ref, base_previous, resolve_prereleases):
        # As we are closing a diamond, there can be conflicts. This will raise if so
        pass

    @staticmethod
    def _prepare_node(node, profile_host, profile_build, down_options, define_consumers=False):
        # basic node configuration: calling configure() and requirements()
        pass

    def _initialize_requires(self, node, graph, graph_lock, profile_build, profile_host):
        pass

    def _resolve_alias(self, node, require, alias, graph):
        # First try cached
        pass

    def _resolve_recipe(self, ref, graph_lock):
        pass

    @staticmethod
    def _resolved_system(node, require, profile_build, profile_host, resolve_prereleases):
        pass

    def _resolve_replace_requires(self, node, require, profile_build, profile_host, graph):
        pass

    @staticmethod
    def _deduce_host_version(require, node):
        pass

    def _create_new_node(self, node, require, graph, profile_host, profile_build, graph_lock):
        pass

    @staticmethod
    def _compute_down_options(node, require, new_ref):
        # The consumer "up_options" are the options that come from downstream to this node
        pass

    @staticmethod
    def _remove_overrides(dep_graph):
        pass

    @staticmethod
    def _remove_orphans(dep_graph):
        # when requires to the same thing with different visible=xxx converge, there can be orphans
        pass
