import os
from typing import List

from conan.cli import make_abs_path
from conan.internal.methods import run_build_method, run_source_method
from conan.internal.graph.graph import CONTEXT_HOST
from conan.internal.graph.profile_node_definer import initialize_conanfile_profile
from conan.internal.errors import conanfile_exception_formatter
from conan.errors import ConanException
from conan.api.model import RecipeReference, Remote
from conan.internal.util.files import chdir


class LocalAPI:
    """ This ``LocalAPI`` contains several helpers related to the local development flow, i.e.,
    locally calling ``source()`` or ``build()`` methods, or adding and removing editable packages
    """

    def __init__(self, conan_api, helpers):
        self._conan_api = conan_api
        self._helpers = helpers

    @staticmethod
    def get_conanfile_path(path, cwd, py):
        """ Obtain the full path to a conanfile file, either .txt or .py, from the current
        working directory.

        If both ``conanfile.py`` and a ``conanfile.txt`` are present, it will raise an error.

        :param path: Relative path to look for the file. Can be a folder or a file.
        :param cwd: The current working directory.
        :param py: If True, a conanfile.py must exist, a .txt is not valid in this case
        """
        pass

    def editable_add(self, path, name=None, version=None, user=None, channel=None, cwd=None,
                     output_folder=None, remotes: List[Remote] = None) -> RecipeReference:
        """ Add the conanfile in the given path as an editable package

        Note that for automation over editables it might be recommended to use the ``WorkspacesAPI``
        instead of this API.

        :param path: Relative path to look for it. Can be a folder or a file.
        :param name: The name of the package. If not defined, it is taken from conanfile
        :param version: The version of the package. If not defined, it is taken from conanfile
        :param user: The user of the package. If not defined, it is taken from conanfile
        :param channel: The channel of the package. If not defined, it is taken from conanfile
        :param cwd: The current working directory
        :param output_folder: The output folder. If not defined, the recipe layout will be used.
        :param remotes: The remotes to resolve possible ``python-requires`` for this recipe if needed.
        :return: RecipeReference of the added package
        """
        pass

    def editable_remove(self, path=None, requires=None, cwd=None):
        """ Remove an editable package from the given path

        Note that for automation over editables it might be recommended to use the ``WorkspacesAPI``
        instead of this API.

        :param path: Relative path to look for it. Can be a folder or a file.
        :param requires: Remove these requirements from editables (instead of by path)
        :param cwd: The current working directory
        :return: RecipeReference of the added package
        """
        pass

    def editable_list(self):
        pass

    def source(self, path, name=None, version=None, user=None, channel=None,
               remotes: List[Remote] = None):
        """ Calls the ``source()`` method of the current (user folder) ``conanfile.py``

        This method does not require computing a dependency graph, because the ``source()``
        method is assumed to be invariant with respect to settings, options and dependencies.

        :param path: Relative path to look for the conanfile. Can be a folder or a file.
        :param name: The name of the package. If not defined, it is taken from conanfile
        :param version: The version of the package. If not defined, it is taken from conanfile
        :param user: The user of the package. If not defined, it is taken from conanfile
        :param channel: The channel of the package. If not defined, it is taken from conanfile
        :param remotes: The remotes to resolve possible ``python-requires`` for this recipe if needed.
        """
        pass

    def build(self, conanfile) -> None:
        """ Calls the ``build()`` method of the current (user folder) ``conanfile.py``

        This method does require computing a dependency graph, because the ``build()`` method
        needs all dependencies and transitive dependencies. Then, the ``conanfile`` argument
        must be the one obtaind from a full dependency graph install operation, including both
        the graph comptutation and the binary installation.

        :param conanfile: ``Conanfile`` object representing the "root" node in the dependency graph,
          corresponding to a ``conanfile.py`` in the user folder, containing the ``build()`` method to
          be called. This ``conanfile`` object must have all of its dependencies computed and
          installed in the current Conan package cache to work.
        """
        pass

    @staticmethod
    def test(conanfile) -> None:
        """ Calls the ``test()`` method of the current (user folder) ``test_package/conanfile.py``

        This method does require computing a dependency graph, because the ``test()`` method
        needs all dependencies and transitive dependencies. Then, the ``conanfile`` argument
        must be the one obtaind from a full dependency graph install operation, including both
        the graph comptutation and the binary installation.

        Typically called after a ``build()`` one.

        :param conanfile: ``Conanfile`` object representing the "root" node in the dependency graph,
          corresponding to a conanfile.py in the user "test_package" folder, containing the ``test()``
          method to be called. This ``conanfile`` object must have all of its dependencies computed
          and installed in the current Conan package cache to work.
        """
        pass

    def inspect(self, conanfile_path, remotes, lockfile, name=None, version=None, user=None,
                channel=None):
        pass
