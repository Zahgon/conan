import json
import os
import textwrap

from conan.api.output import ConanOutput
from conan.internal.graph.graph import RECIPE_CONSUMER, RECIPE_VIRTUAL, BINARY_SKIP, \
    BINARY_MISSING, BINARY_INVALID, Overrides, BINARY_BUILD, BINARY_EDITABLE_BUILD, BINARY_PLATFORM
from conan.errors import ConanException, ConanInvalidConfiguration
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.files import load


class _InstallPackageReference:
    """ Represents a single, unique PackageReference to be downloaded, built, etc.
    Same PREF should only be built or downloaded once, but it is possible to have multiple
    nodes in the DepsGraph that share the same PREF.
    PREF could have PREV if to be downloaded (must be the same for all), but won't if to be built
    """
    def __init__(self):
        self.package_id = None
        self.prev = None
        self.nodes = []  # GraphNode
        self.binary = None  # The action BINARY_DOWNLOAD, etc must be the same for all nodes
        self.context = None  # Same PREF could be in both contexts, but only 1 context is enough to
        # be able to reproduce, typically host preferrably
        self.options = []  # to be able to fire a build, the options will be necessary
        self.filenames = []  # The build_order.json filenames e.g. "windows_build_order"
        # If some package, like ICU, requires itself, built for the "build" context architecture
        # to cross compile, there will be a dependency from the current "self" (host context)
        # to that "build" package_id.
        self.depends = []  # List of package_ids of dependencies to other binaries of the same ref
        self.overrides = Overrides()
        self.ref = None
        self.info = None

    @property
    def pref(self):
        pass

    @property
    def conanfile(self):
        pass

    @staticmethod
    def create(node):
        pass

    def add(self, node):
        pass

    def _build_args(self):
        pass

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data, filename, ref):
        pass


class _InstallRecipeReference:
    """ represents a single, unique Recipe reference (including revision, must have it) containing
    all the _InstallPackageReference that belongs to this RecipeReference. This approach is
    oriented towards a user-intuitive grouping specially in CI, in which all binary variants for the
    same recipe revision (repo+commit) are to be built grouped together"""
    def __init__(self):
        self.ref = None
        self._node = None
        self.packages = {}  # {package_id: _InstallPackageReference}
        self.depends = []  # Other REFs, defines the graph topology and operation ordering

    def __str__(self):
        return f"{self.ref} ({self._node.binary}) -> {[str(d) for d in self.depends]}"

    @property
    def need_build(self):
        pass

    def reduce(self):
        pass

    @property
    def node(self):
        pass

    @staticmethod
    def create(node):
        pass

    def merge(self, other):
        pass

    def add(self, node):
        pass

    def _install_order(self):
        # TODO: Repeated, refactor
        # a topological order by levels, returns a list of list, in order of processing
        pass

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data, filename):
        pass


class _InstallConfiguration:
    """ Represents a single, unique PackageReference to be downloaded, built, etc.
    Same PREF should only be built or downloaded once, but it is possible to have multiple
    nodes in the DepsGraph that share the same PREF.
    PREF could have PREV if to be downloaded (must be the same for all), but won't if to be built
    """
    def __init__(self):
        self.ref = None
        self.package_id = None
        self.prev = None
        self.nodes = []  # GraphNode
        self.binary = None  # The action BINARY_DOWNLOAD, etc must be the same for all nodes
        self.context = None  # Same PREF could be in both contexts, but only 1 context is enough to
        # be able to reproduce, typically host preferrably
        self.options = []  # to be able to fire a build, the options will be necessary
        self.filenames = []  # The build_order.json filenames e.g. "windows_build_order"
        self.depends = []  # List of full prefs
        self.overrides = Overrides()
        self.info = None

    def __str__(self):
        return f"{self.ref}:{self.package_id} ({self.binary}) -> {[str(d) for d in self.depends]}"

    @property
    def need_build(self):
        pass

    def reduce(self):
        pass

    @property
    def pref(self):
        pass

    @property
    def conanfile(self):
        pass

    @staticmethod
    def create(node):
        pass

    def add(self, node):
        pass

    def _build_args(self):
        pass

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data, filename):
        pass

    def merge(self, other):
        pass


class ProfileArgs:
    def __init__(self, args):
        self._args = args

    @staticmethod
    def from_args(args):
        pass

    def __str__(self):
        return self._args

    @staticmethod
    def deserialize(data):
        pass

    def serialize(self):
        pass


class InstallGraph:
    """ A graph containing the package references in order to be built/downloaded
    """

    def __init__(self, deps_graph, order_by=None, profile_args=None):
        self._nodes = {}  # ref with rev: _InstallGraphNode
        order_by = order_by or "recipe"
        self._order = order_by
        self._node_cls = _InstallRecipeReference if order_by == "recipe" else _InstallConfiguration
        self._is_test_package = False
        self.reduced = False
        self._profiles = {"self": profile_args} if profile_args is not None else {}
        self._filename = None
        if deps_graph is not None:
            self._initialize_deps_graph(deps_graph)
            self._is_test_package = deps_graph.root.conanfile.tested_reference_str is not None

    @staticmethod
    def load(filename):
        pass

    def merge(self, other):
        """
        :type other: InstallGraph
        """
        pass

    @staticmethod
    def deserialize(data, filename):
        pass

    def _initialize_deps_graph(self, deps_graph):
        pass

    def reduce(self):
        pass

    def install_order(self, flat=False):
        # a topological order by levels, returns a list of list, in order of processing
        pass

    @staticmethod
    def _raise_loop_detected(nodes):
        """
        We can exclude the nodes that have already been processed they do not content loops
        """
        pass

    def install_build_order(self):
        # TODO: Rename to serialize()?
        """ used for graph build-order and graph build-order-merge commands
        This is basically a serialization of the build-order
        """
        pass

    def _get_missing_invalid_packages(self):
        pass

    def raise_errors(self):
        pass

    def get_errors(self):
        pass

    @staticmethod
    def _raise_invalid(invalid):
        pass

    def _raise_missing(self, missing):
        # TODO: Remove out argument
        # TODO: A bit dirty access to .pref
        pass
