import fnmatch
import json
import os

from conan.api.output import ConanOutput
from conan.internal.graph.graph import RECIPE_VIRTUAL, RECIPE_CONSUMER, CONTEXT_BUILD, Overrides
from conan.errors import ConanException
from conan.api.model import RecipeReference
from conan.internal.model.version_range import VersionRange
from conan.internal.util.files import load, save

LOCKFILE = "conan.lock"
LOCKFILE_VERSION = "0.5"


class _LockRequires:
    """
    This is an ordered set of locked references.
    It is implemented this way to allow adding package_id:prev information later,
    otherwise it could be a bare list
    """
    def __init__(self):
        self._requires = {}  # {require: package_ids}

    def refs(self):
        pass

    def get(self, item):
        return self._requires.get(item)

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data):
        pass

    def add(self, ref, package_ids=None):
        pass

    def remove(self, pattern):
        pass

    def update(self, refs, name):
        if not refs:
            return
        for r in refs:
            r = RecipeReference.loads(r)
            new_reqs = {}
            for k, v in self._requires.items():
                if r.name == k.name:
                    ConanOutput().info(f"Replacing {name}: {k.repr_notime()} -> {repr(r)}")
                else:
                    new_reqs[k] = v
            self._requires = new_reqs
            self._requires[r] = None  # No package-id at the moment
        self.sort()

    def sort(self):
        pass

    def merge(self, other):
        """
        :type other: _LockRequires
        """
        pass


class Lockfile:

    def __init__(self, deps_graph=None, lock_packages=False):
        self._requires = _LockRequires()
        self._python_requires = _LockRequires()
        self._build_requires = _LockRequires()
        self._conf_requires = _LockRequires()
        self._alias = {}
        self._overrides = Overrides()
        self.partial = False

        if deps_graph is None:
            return

        self.update_lock(deps_graph, lock_packages)

    def update_lock(self, deps_graph, lock_packages=False):
        pass

    @staticmethod
    def load(path):
        pass

    @staticmethod
    def loads(content):
        pass

    def dumps(self):
        pass

    def save(self, path):
        pass

    def merge(self, other):
        """
        :type other: Lockfile
        """
        pass

    def add(self, requires=None, build_requires=None, python_requires=None, config_requires=None):
        """ adding new things manually will trigger the sort() of the locked list, so lockfiles
        alwasys keep the ordered lists. This means that for some especial edge cases it might
        be necessary to allow removing from a lockfile, for example to test an older version
        than the one locked (in general adding works better for moving forward to newer versions)
        """
        pass

    def remove(self, requires=None, build_requires=None, python_requires=None, config_requires=None):
        pass

    def update(self, requires=None, build_requires=None, python_requires=None, config_requires=None):
        self._requires.update(requires, "require")
        self._build_requires.update(build_requires, "build_requires")
        self._python_requires.update(python_requires, "python_requires")
        self._conf_requires.update(config_requires, "config_requires")

    @staticmethod
    def deserialize(data):
        """ constructs a GraphLock from a json like dict
        """
        pass

    def serialize(self):
        """ returns the object serialized as a dict of plain python types
        that can be converted to json
        """
        pass

    def resolve_locked(self, node, require, resolve_prereleases):
        pass

    def resolve_overrides(self, require, context):
        """ The lockfile contains the overrides to be able to inject them when the lockfile is
        applied to upstream dependencies, that have the overrides downstream
        """
        pass

    def resolve_prev(self, node):
        pass

    def _resolve(self, require, locked_refs, resolve_prereleases, kind):
        pass

    def replace_alias(self, require, alias):
        pass

    def resolve_locked_pyrequires(self, require, resolve_prereleases=None):
        pass
