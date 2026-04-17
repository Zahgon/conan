import os

from conan.errors import ConanException
from conan.api.model import RecipeReference
from conan.internal.model.requires import Requirement


class PyRequire:
    def __init__(self, module, conanfile, ref, path, recipe_status, remote):
        self.module = module
        self.conanfile = conanfile
        self.ref = ref
        self.path = path
        self.recipe = recipe_status
        self.remote = remote

    def serialize(self):
        pass


class PyRequires:
    """ this is the object that replaces the declared conanfile.py_requires"""
    def __init__(self):
        self._pyrequires = {}  # {pkg-name: PythonRequire}

    def serialize(self):
        pass

    def all_refs(self):
        pass

    def info_requires(self):
        pass

    def items(self):
        return self._pyrequires.items()

    def __getitem__(self, item):
        try:
            return self._pyrequires[item]
        except KeyError:
            raise ConanException("'%s' is not a python_require" % item)

    def add_pyrequire(self, py_require):
        pass


class PyRequireLoader:
    def __init__(self, proxy, range_resolver, global_conf):
        self._proxy = proxy
        self._range_resolver = range_resolver
        self._cached_py_requires = {}
        self._resolve_prereleases = global_conf.get("core.version_ranges:resolve_prereleases")

    def load_py_requires(self, conanfile, loader, graph_lock, remotes, update, check_update):
        pass

    def _resolve_py_requires(self, py_requires_refs, graph_lock, loader, remotes, update,
                             check_update):
        pass

    def _resolve_ref(self, requirement, graph_lock, remotes, update):
        pass

    def _load_pyreq_conanfile(self, loader, graph_lock, ref, remotes, update, check_update):
        pass
