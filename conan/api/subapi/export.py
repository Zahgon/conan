import os
from typing import List, Tuple

from conan import ConanFile
from conan.api.output import ConanOutput
from conan.cli.printers.graph import print_graph_basic
from conan.internal.cache.cache import PkgCache
from conan.internal.api.export import cmd_export
from conan.internal.methods import run_package_method
from conan.internal.graph.graph import BINARY_BUILD, RECIPE_INCACHE
from conan.api.model import PkgReference, Remote, RecipeReference
from conan.internal.util.files import mkdir


class ExportAPI:
    """ This API provides methods to export artifacts, both recipes and pre-compiled package
    binaries from user folders to the Conan cache, as Conan recipes and Conan package binaries
    """

    def __init__(self, conan_api, helpers):
        self._conan_api = conan_api
        self._helpers = helpers

    def export(self, path, name: str = None, version: str = None, user: str = None,
               channel: str = None, lockfile=None,
               remotes: List[Remote] = None) -> Tuple[RecipeReference, ConanFile]:
        """ Exports a ``conanfile.py`` recipe, together with its associated files to the Conan cache.
        A "recipe-revision" will be computed and assigned.

        :param path: Path to the conanfile to be exported
        :param name: Optional package name. Typically not necessary as it is defined by the recipe
            attribute or dynamically with the ``set_name()`` method.
            If it is defined in recipe and as an argument, but they don't match, an error will be raised.
        :param version: Optional version. It can be defined in the recipe with the version
            attribute or dynamically with the 'set_version()' method.
            If it is defined in recipe and as an argument, but they don't match, an error will be raised.
        :param user: Optional user. Can be defined by recipe attribute.
            If it is defined in recipe and as an argument, but they don't match, an error will be raised.
        :param channel: Optional channel. Can be defined by recipe attribute.
            If it is defined in recipe and as an argument, but they don't match, an error will be raised.
        :param lockfile: Optional, only relevant if the recipe has 'python-requires' to be locked
        :param remotes: Optional, only relevant to resolve 'python-requires' in remotes
        :return: A tuple of the exported RecipeReference and a ConanFile object
        """
        pass

    def export_pkg_graph(self, path, ref: RecipeReference, profile_host, profile_build,
                         remotes: List[Remote], lockfile=None, is_build_require=False,
                         skip_binaries=False, output_folder=None):
        """Computes a dependency graph for a given configuration, for an already existing (previously
        exported) recipe in the Conan cache. This method computes the full dependency graph, using
        the profiles, lockfile and remotes information as any other install/graph/create command.
        This is necessary in order to compute the "package_id" of the binary being exported
        into the Conan cache.
        The resulting dependency graph can be passed to ``export_pkg()`` method

        :param path: Path to the conanfile.py in the user folder
        :param ref: full RecipeReference, including recipe-revision
        :param profile_host: Profile for the host context
        :param profile_build: Profile for the build context
        :param lockfile: Optional lockfile
        :param remotes: List of Remotes
        :param is_build_require: In case a package intended to be used as a tool-requires
        :param skip_binaries:
        :param output_folder: The folder containing output files, like potential environment scripts
        :return: A Graph object that can be passed to ``export_pkg()`` method
        """
        pass

    def export_pkg(self, graph, output_folder=None) -> None:
        """Executes the ``package()`` method of the exported recipe in order to copy the artifacts
        from user folder to the Conan cache package folder

        :param graph: A Graph object
        :param output_folder: Optional folder where generated files like environment scripts
            of dependencies have been installed
        """
        pass
