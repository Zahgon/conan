import os
import shutil

import yaml

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.errors import scoped_traceback
from conan.internal.util.files import load, save

# Related folder
WORKSPACE_FOLDER = "conanws"
# Related files
WORKSPACE_YML = "conanws.yml"
WORKSPACE_PY = "conanws.py"


class Workspace:
    """
    The base class for all workspaces
    """

    def __init__(self, folder, conan_api):
        self.folder = folder
        self.conan_data = self._conan_load_data()
        self._conan_api = conan_api
        self.output = ConanOutput(scope=f"Workspace '{self.name()}'")

    def __getattribute__(self, item):
        # Return a protected wrapper around workspace overridable callables in order to
        # be able to have clean errors if user errors in conanws.py code
        myattr = object.__getattribute__(self, item)
        if item not in ("name", "packages", "add", "remove", "clean", "build_order"):
            return myattr

        def wrapper(*args, **kwargs):
            pass
        return wrapper

    def name(self):
        pass

    def _conan_load_data(self):
        pass

    def add(self, ref, path, output_folder):
        pass

    def remove(self, path):
        pass

    def clean(self):
        pass

    def _conan_rel_path(self, path):
        pass

    def packages(self):
        pass

    def load_conanfile(self, conanfile_path):
        pass

    def root_conanfile(self):  # noqa
        pass

    def build_order(self, order):  # noqa
        pass
