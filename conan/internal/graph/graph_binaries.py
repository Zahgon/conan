import os

from conan.api.output import ConanOutput, Color
from conan.internal.cache.home_paths import HomePaths
from conan.internal.graph.build_mode import BuildMode
from conan.internal.graph.compatibility import BinaryCompatibility
from conan.internal.graph.compute_pid import compute_package_id
from conan.internal.graph.graph import (BINARY_BUILD, BINARY_CACHE, BINARY_DOWNLOAD, BINARY_MISSING,
                                        BINARY_UPDATE, RECIPE_EDITABLE, BINARY_EDITABLE,
                                        RECIPE_CONSUMER, RECIPE_VIRTUAL, BINARY_SKIP,
                                        BINARY_INVALID, BINARY_EDITABLE_BUILD, RECIPE_PLATFORM,
                                        BINARY_PLATFORM)
from conan.internal.graph.proxy import should_update_reference
from conan.internal.errors import (conanfile_exception_formatter, ConanConnectionError,
                                   NotFoundException, PackageNotFoundException)
from conan.errors import ConanException
from conan.internal.model.conanconfig import loadconanconfig
from conan.internal.model.info import RequirementInfo, RequirementsInfo
from conan.internal.model.pkg_type import PackageType


class GraphBinariesAnalyzer:

    def __init__(self, cache, remote_manager, home_folder, global_conf, hook_manager):
        self._cache = cache
        self._home_folder = home_folder
        self._global_conf = global_conf
        self._remote_manager = remote_manager
        self._hook_manager = hook_manager
        # These are the nodes with pref (not including PREV) that have been evaluated
        self._evaluated = {}  # {pref: [nodes]}
        compat_folder = HomePaths(home_folder).compatibility_plugin_path
        self._compatibility = BinaryCompatibility(compat_folder, hook_manager)
        unknown_mode = global_conf.get("core.package_id:default_unknown_mode", default="semver_mode")
        non_embed = global_conf.get("core.package_id:default_non_embed_mode", default="minor_mode")
        # recipe_revision_mode already takes into account the package_id
        embed_mode = global_conf.get("core.package_id:default_embed_mode", default="full_mode")
        python_mode = global_conf.get("core.package_id:default_python_mode", default="minor_mode")
        build_mode = global_conf.get("core.package_id:default_build_mode", default=None)
        self._modes = unknown_mode, non_embed, embed_mode, python_mode, build_mode
        self._warn_about_new_compatibility = False

    @staticmethod
    def _evaluate_build(node, build_mode):
        pass

    @staticmethod
    def _evaluate_clean_pkg_folder_dirty(node, package_layout):
        # Check if dirty, to remove it
        pass

    # check through all the selected remotes:
    # - if not --update: get the first package found
    # - if --update: get the latest remote searching in all of them
    def _get_package_from_remotes(self, node, remotes, update):
        pass

    def _evaluate_is_cached(self, node):
        """ Each pref has to be evaluated just once, and the action for all of them should be
        exactly the same
        """
        pass

    def _compatible_get_packages(self, node):
        # Evaluate the ``compatibility() methods to compute the compatible hypothesis variants
        pass

    @staticmethod
    def _compatible_found(conanfile, pkg_id, compatible_pkg):
        pass

    def _compatible_find_existing_binaries(self, node, compatibles, remotes, update):
        # Do the actual search in the cache and remotes for the compatible package-ids
        pass

    def _compatible_cache_latest_prev(self, node):
        """ simplified checking of compatible_packages, that should be found existing, but
        will never be built, for example. They cannot be editable either at this point.
        """
        pass

    @staticmethod
    def _binary_in_cache(node, cache_latest_prev):
        pass

    def _compatible_get_packages_from_remotes(self, ref, remotes):
        """
        Get available package ids in remotes for the given node reference
        """
        pass

    def _compatible_find_build_binary(self, node, compatibles):
        pass

    def _evaluate_node(self, node, build_mode, remotes, update):
        pass

    def _process_node(self, node, build_mode, remotes, update):
        pass

    def _process_locked_node(self, node, build_mode, locked_prev):
        # Check that this same reference hasn't already been checked
        pass

        # TODO: Check in remotes for download

    def _evaluate_download(self, node, remotes, update):
        pass

    def _evaluate_cache_update(self, cache_latest_prev, node, remotes, update):
        pass

    def _config_version(self):
        pass

    def _evaluate_package_id(self, node, config_version):
        pass

    def evaluate_graph(self, deps_graph, build_mode, lockfile, remotes, update, build_mode_test=None,
                       tested_graph=None):
        pass

    @staticmethod
    def _skip_binaries(graph):
        pass
