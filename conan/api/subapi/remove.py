from typing import Optional

from conan.api.model import Remote
from conan.api.model import PkgReference
from conan.api.model import RecipeReference


class RemoveAPI:

    def __init__(self, conan_api, api_helpers):
        self._conan_api = conan_api
        self._api_helpers = api_helpers

    def recipe(self, ref: RecipeReference, remote: Optional[Remote] = None):
        pass

    def all_recipe_packages(self, ref: RecipeReference, remote: Optional[Remote] = None):
        pass

    def _remove_all_local_packages(self, ref):
        # Get all the prefs and all the prevs
        pass

    def package(self, pref: PkgReference, remote: Optional[Remote]):
        pass
