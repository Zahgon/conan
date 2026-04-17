from collections import OrderedDict

from conan.internal.graph.graph_error import GraphError, GraphConflictError
from conan.api.output import ConanOutput
from conan.api.model import PkgReference
from conan.api.model import RecipeReference

RECIPE_DOWNLOADED = "Downloaded"
RECIPE_INCACHE = "Cache"  # The previously installed recipe in cache is being used
RECIPE_UPDATED = "Updated"
RECIPE_INCACHE_DATE_UPDATED = "Cache (Updated date)"
RECIPE_NEWER = "Newer"  # The local recipe is  modified and newer timestamp than server
RECIPE_NOT_IN_REMOTE = "Not in remote"
RECIPE_UPDATEABLE = "Update available"  # The update of recipe is available (only in conan info)
# These recipes do not have a full reference, not in the cache
RECIPE_EDITABLE = "Editable"
RECIPE_CONSUMER = "Consumer"  # A conanfile from the user
RECIPE_VIRTUAL = "Cli"  # A virtual conanfile (dynamic in memory conanfile)
RECIPE_PLATFORM = "Platform"

BINARY_CACHE = "Cache"
BINARY_DOWNLOAD = "Download"
BINARY_UPDATE = "Update"
BINARY_BUILD = "Build"
BINARY_MISSING = "Missing"
BINARY_SKIP = "Skip"
BINARY_EDITABLE = "Editable"
BINARY_EDITABLE_BUILD = "EditableBuild"
BINARY_INVALID = "Invalid"
BINARY_PLATFORM = "Platform"

CONTEXT_HOST = "host"
CONTEXT_BUILD = "build"


class TransitiveRequirement:
    def __init__(self, require, node):
        self.require = require
        self.node = node

    def __repr__(self):
        return "Require: {}, Node: {}".format(repr(self.require), repr(self.node))


class Node:

    def __init__(self, ref, conanfile, context, recipe=None, path=None, test=False):
        self.ref = ref
        self.path = path  # path to the consumer conanfile.xx for consumer, None otherwise
        self._package_id = None
        self.prev = None
        self.pref_timestamp = None
        if conanfile is not None:
            conanfile._conan_node = self  # Reference to self, to access data
        self.conanfile = conanfile

        self.binary = None
        self.recipe = recipe
        self.remote = None
        self.binary_remote = None
        self.context = context
        self.test = test

        # real graph model
        self.transitive_deps = OrderedDict()  # of _TransitiveRequirement
        self.edges = []  # Ordered Edges
        self.dependants = []  # Edges
        self.error = None
        self.should_build = False  # If the --build or policy wants to build this binary
        self.build_allowed = False
        self.is_conf = False
        self.replaced_requires = {}  # To track the replaced requires for self.edges[old-ref]
        self.skipped_build_requires = False
        self.editable_output_folder = None  # In case this node is editable

    @property
    def dependencies(self):
        pass

    def subgraph(self):
        pass

    def __lt__(self, other):
        """
        :type other: Node
        """
        # TODO: Remove this order, shouldn't be necessary
        return (str(self.ref), self._package_id) < (str(other.ref), other._package_id)

    def propagate_closing_loop(self, require, prev_node, visibility_conflicts):
        pass

    def propagate_downstream(self, require, node, visibility_conflicts, src_node=None):
        # print("  Propagating downstream ", self, "<-", require)
        pass

    def check_downstream_exists(self, require):
        # First, a check against self, could be a loop-conflict
        # This is equivalent as the Requirement hash and eq methods
        # TODO: Make self.ref always exist, but with name=None if name not defined
        pass

    def check_loops(self, new_node, count=0):
        pass

    @property
    def package_id(self):
        pass

    @package_id.setter
    def package_id(self, pkg_id):
        pass

    @property
    def name(self):
        pass

    @property
    def pref(self):
        pass

    def add_edge(self, edge):
        pass

    def neighbors(self):
        pass

    def inverse_neighbors(self):
        pass

    def __repr__(self):
        return repr(self.conanfile)

    def serialize(self):
        pass

    def overrides(self):

        pass


class Edge:
    def __init__(self, src, dst, require):
        self.src = src
        self.dst = dst
        self.require = require


class Overrides:
    def __init__(self):
        self._overrides = {}  # {require_ref: {override_ref1, override_ref2}}

    def __bool__(self):
        return bool(self._overrides)

    def __repr__(self):
        return repr(self.serialize())

    @staticmethod
    def create(nodes):
        pass

    def get(self, require):
        return self._overrides.get(require)

    def update(self, other):
        """
        :type other: Overrides
        """
        for require, override_info in other._overrides.items():
            self._overrides.setdefault(require, set()).update(override_info)

    def items(self):
        return self._overrides.items()

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data):
        pass


class DepsGraph:
    def __init__(self):
        self.nodes = []
        self.aliased = {}
        self.resolved_ranges = {}
        self.replaced_requires = {}
        self.options_conflicts = {}
        self.visibility_conflicts = {}
        self.error = False

    def lockfile(self):
        pass

    def overrides(self):
        pass

    def __repr__(self):
        return "\n".join((repr(n) for n in self.nodes))

    @property
    def root(self):
        pass

    def add_node(self, node):
        pass

    @staticmethod
    def add_edge(src, dst, require):
        pass

    def ordered_iterate(self):
        pass

    def by_levels(self):
        """ order by node degree. The first level will be the one which nodes dont have
        dependencies. Second level will be with nodes that only have dependencies to
        first level nodes, and so on
        return [[node1, node34], [node3], [node23, node8],...]
        """
        pass

    def report_graph_error(self):
        pass

    def serialize(self):
        pass
