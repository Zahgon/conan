import copy
import fnmatch
import json
import os
from os.path import join, normpath

from conan.api.model import RecipeReference
from conan.internal.util.files import load, save


EDITABLE_PACKAGES_FILE = 'editable_packages.json'


class EditablePackages:
    def __init__(self, cache_folder=None):
        if cache_folder is None:
            self._edited_refs = {}
            return
        self._edited_file = normpath(join(cache_folder, EDITABLE_PACKAGES_FILE))
        if os.path.exists(self._edited_file):
            edited = load(self._edited_file)
            edited_js = json.loads(edited)
            self._edited_refs = {RecipeReference.loads(r): d
                                 for r, d in edited_js.items()}
        else:
            self._edited_refs = {}  # {ref: {"path": path, "layout": layout}}

    def update_copy(self, ws_editables):
        """
        Create a new instance with the union of the editable packages of self and other
        """
        pass

    @property
    def edited_refs(self):
        pass

    def save(self):
        pass

    def get(self, ref):
        _tmp = copy.copy(ref)
        _tmp.revision = None
        return self._edited_refs.get(_tmp)

    def add(self, ref, path, output_folder=None):
        pass

    def remove(self, path, requires):
        pass
