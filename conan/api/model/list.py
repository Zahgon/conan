import copy
import fnmatch
import json
import os
from json import JSONDecodeError
from typing import Iterable, Tuple, Dict

from conan.api.model import RecipeReference, PkgReference
from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.errors import NotFoundException
from conan.internal.model.version_range import VersionRange
from conan.internal.graph.graph import RECIPE_EDITABLE, RECIPE_CONSUMER, RECIPE_PLATFORM, \
    RECIPE_VIRTUAL, BINARY_SKIP, BINARY_MISSING, BINARY_INVALID
from conan.internal.util.files import load


class MultiPackagesList:
    """ A collection of PackagesList by remote name."""
    def __init__(self):
        self.lists = {}

    def __getitem__(self, name):
        try:
            return self.lists[name]
        except KeyError:
            raise ConanException(f"'{name}' doesn't exist in package list")

    def add(self, name, pkg_list):
        pass

    def add_error(self, remote_name, error):
        pass

    def serialize(self):
        """ Serialize object to a dictionary."""
        pass

    def merge(self, other):
        pass

    @staticmethod
    def load(file):
        """ Create an instance of the class from a serialized JSON file path pointed by ``file``."""
        pass

    @staticmethod
    def load_graph(graphfile, graph_recipes=None, graph_binaries=None, context=None):
        """ Create an instance of the class from a graph file path, which is
        the json format returned by a few commands
        like ``conan graph info`` or ``conan create/install.``

        :parameter str graphfile: Path to the graph file
        :parameter list[str] graph_recipes: List for kinds of recipes to return.
            For example ``"cache"`` will return only recipes in the local cache,
            ``"download"`` will return only recipes that have been downloaded,
            and passing ``"*"`` will return all recipes.
        :parameter list[str] graph_binaries: List for kinds of binaries to return.
            For example ``"cache"`` will return only binaries in the local cache,
            ``"download"`` will return only binaries that have been downloaded,
            ``"build"`` will return only binaries that are built,
            ``"missing"`` will return only binaries that are missing,
            ``"invalid"`` will return only binaries that are invalid,
            and passing ``"*"`` will return all binaries.
        :parameter str context: Context to filter the graph,
            can be ``"host"``, ``"build"``, ``"host-only"`` or ``"build-only"``
        """
        pass

    @staticmethod
    def _define_graph(graph, graph_recipes=None, graph_binaries=None, context=None):
        pass

    @staticmethod
    def _filter_exclusive_context(mpkglist, graph, context):
        pass


class PackagesList:
    """ A collection of recipes, revisions and packages."""
    def __init__(self):
        self._data = {}

    def __bool__(self):
        """ Whether the package list contains any recipe"""
        return bool(self._data)

    def merge(self, other):
        pass

    def split(self):
        """
        Returns a list of PackageList, split one per reference.
        This can be useful to parallelize things like upload, parallelizing per-reference
        """
        pass

    def only_recipes(self) -> None:
        """ Filter out all the packages and package revisions, keep only the recipes and
            recipe revisions in self._data.
        """
        pass

    def add_refs(self, refs):
        pass

    def add_ref(self, ref: RecipeReference) -> None:
        """
        Adds a new RecipeReference to a package list
        """
        pass

    def add_prefs(self, rrev, prefs):
        pass

    def add_pref(self, pref: PkgReference, pkg_info: dict = None) -> None:
        """
        Add a PkgReference to an already existing RecipeReference inside a package list
        """
        pass

    def add_configurations(self, confs):
        pass

    def refs(self):
        pass

    def items(self) -> Iterable[Tuple[RecipeReference, Dict[PkgReference, Dict]]]:
        """Iterate over the contents of the package list.

        Yields tuples containing a recipe reference and a dictionary of its
        associated package references content.

        Returns:
            An iterable of tuples where:

            - The first element is a ``RecipeReference`` (representing the recipe revision).
            - The second element is a dictionary mapping a ``PkgReference`` to a nested dictionary of
              its specific attributes (e.g., settings, options).

        Warning:
            **Missing Revisions Behavior:**
            This method filters out results that lack revision information.

            - It will ONLY yield items if they contain at least a **recipe revision**.
            - The nested package dictionary will be empty unless it contains a **package revision**.

            **When to use serialize instead:**
            If you perform a general search that does not fetch revisions (e.g., running
            ``conan list *``), this method will yield nothing because no artifact references
            are created. In these cases, use the ``serialize()`` method to access the results.

            To successfully use ``items()``, your query must explicitly request revisions
            (e.g., running ``conan list pkg/version#*:*#*``).
        """
        for ref, ref_dict in self._data.items():
            for rrev, rrev_dict in ref_dict.get("revisions", {}).items():
                recipe = RecipeReference.loads(f"{ref}#{rrev}")  # TODO: optimize this
                t = rrev_dict.get("timestamp")
                if t is not None:
                    recipe.timestamp = t
                packages = {}
                for package_id, pkg_info in rrev_dict.get("packages", {}).items():
                    prevs = pkg_info.get("revisions", {})
                    for prev, prev_info in prevs.items():
                        t = prev_info.get("timestamp")
                        pref = PkgReference(recipe, package_id, prev, t)
                        packages[pref] = prev_info
                yield recipe, packages

    def recipe_dict(self, ref: RecipeReference):
        """ Gives read/write access to the dictionary containing a specific RecipeReference
        information.
        """
        pass

    def has_rref(self, ref: RecipeReference) -> bool:
        # Checks if the PackagesList contains the given RecipeReference.
        pass

    def package_dict(self, pref: PkgReference):
        """ Gives read/write access to the dictionary containing a specific PkgReference
        information
        """
        pass

    @staticmethod
    def prefs(ref, recipe_bundle):
        pass

    def serialize(self):
        """ Serialize the instance to a dictionary."""
        pass

    @staticmethod
    def deserialize(data):
        """ Loads the data from a serialized dictionary."""
        pass


class ListPattern:
    """ Object holding a pattern that matches recipes, revisions and packages."""

    def __init__(self, expression, rrev="latest", package_id=None, prev="latest", only_recipe=False):
        """
        :param expression: The pattern to match, e.g. ``"name/*:*"``
        :param rrev: The recipe revision to match, defaults to ``"latest"``,
                     can also be ``"!latest"`` or ``"~latest"`` to match all but the latest revision,
                     a pattern like ``"1234*"`` to match a specific revision,
                     or a specific revision like ``"1234"``.
        :param package_id: The package ID to match, defaults to ``None``, which matches all package IDs.
        :param prev: The package revision to match, defaults to ``"latest"``,
                     can also be ``"!latest"`` or ``"~latest"`` to match all but the latest revision,
                     a pattern like ``"1234*"`` to match a specific revision,
                     or a specific revision like ``"1234"``.
        :param only_recipe: If ``True``, only the recipe part of the expression is parsed,
                            ignoring ``package_id`` and ``prev``. This is useful for commands that
                            only operate on recipes, like ``conan search``.
        """
        def split(s, c, default=None):
            pass

        recipe, package = split(expression, ":")
        self.raw = expression
        self.ref, rrev = split(recipe, "#", rrev)
        ref, user_channel = split(self.ref, "@")
        self.name, self.version = split(ref, "/")
        self.user, self.channel = split(user_channel, "/")
        self.rrev, _ = split(rrev, "%")
        self.package_id, prev = split(package, "#", prev)
        self.prev, _ = split(prev, "%")
        if only_recipe:
            if self.package_id:
                raise ConanException("Do not specify 'package_id' with 'only-recipe'")
        else:
            self.package_id = self.package_id or package_id

    @staticmethod
    def _only_latest(rev):
        pass

    @property
    def search_ref(self):
        pass

    @property
    def _version_range(self):
        pass

    def filter_versions(self, refs, resolve_prereleases=None):
        pass

    @property
    def is_latest_rrev(self):
        pass

    @property
    def is_latest_prev(self):
        pass

    def check_refs(self, refs):
        pass

    def filter_rrevs(self, rrevs):
        pass

    def filter_prefs(self, prefs):
        pass

    def filter_prevs(self, prevs):
        pass
