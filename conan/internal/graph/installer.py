import os
import shutil
from multiprocessing.pool import ThreadPool

from conan.api.output import ConanOutput, Color
from conan.internal.methods import run_build_method, run_package_method
from conan.internal.api.install.generators import write_generators
from conan.internal.graph.graph import (BINARY_BUILD, BINARY_CACHE, BINARY_DOWNLOAD,
                                        BINARY_EDITABLE, BINARY_UPDATE, BINARY_EDITABLE_BUILD,
                                        BINARY_SKIP)
from conan.internal.graph.install_graph import InstallGraph
from conan.internal.source import retrieve_exports_sources, config_source
from conan.internal.errors import conanfile_remove_attr, conanfile_exception_formatter
from conan.errors import ConanException
from conan.internal.model.cpp_info import CppInfo, MockInfoProperty
from conan.api.model import PkgReference
from conan.internal.paths import CONANINFO
from conan.internal.util import cpu_count
from conan.internal.util.files import clean_dirty, is_dirty, mkdir, rmdir, save, set_dirty, chdir


def build_id(conan_file):
    pass


class _PackageBuilder:

    def __init__(self, cache, remote_manager, cache_folder, hook_manager):
        self._cache = cache
        self._hook_manager = hook_manager
        self._remote_manager = remote_manager
        self._home_folder = cache_folder

    def _get_build_folder(self, conanfile, package_layout):
        # Build folder can use a different package_ID if build_id() is defined.
        # This function decides if the build folder should be re-used (not build again)
        # and returns the build folder
        pass

    @staticmethod
    def _copy_sources(conanfile, source_folder, build_folder):
        # Copies the sources to the build-folder, unless no_copy_source is defined
        pass

    def _build(self, conanfile, pref):
        pass

    def _package(self, conanfile, pref):
        # Creating ***info.txt files
        pass

    def build_package(self, node, recipe_layout, package_layout):
        pass


class BinaryInstaller:
    """ main responsible of retrieving binary packages or building them from source
    locally in case they are not found in remotes
    """

    def __init__(self, api, global_conf, hook_manager):
        helpers = api._api_helpers  # noqa
        self._cache = helpers.cache
        self._remote_manager = helpers.remote_manager
        self._hook_manager = hook_manager
        self._global_conf = global_conf
        self._home_folder = api.home_folder

    def _install_source(self, node, remotes, need_conf=False):
        pass

    @staticmethod
    def install_system_requires(graph, only_info=False, install_order=None):
        pass

    def install_sources(self, graph, remotes):
        pass

    def install(self, deps_graph, remotes, install_order=None):
        pass

    def _download_bulk(self, install_order):
        """ executes the download of packages (both download and update), only once for a given
        PREF
        """
        pass

    def _download_pkg(self, package):
        pass

    def _handle_package(self, recipe_layout, package, install_reference, handled_count, total_count):
        pass

    def _handle_node_editable(self, install_node):
        # It will only run generation
        pass

    def _handle_node_build(self, package, recipe_layout, pkg_layout):
        pass

    def _call_package_info(self, conanfile, package_folder, is_editable):

        pass

    @staticmethod
    def _call_finalize_method(conanfile, finalize_folder):
        pass
