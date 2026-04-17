from urllib.parse import urlencode

from conan.api.model import RecipeReference
from conan.internal.rest.rest_routes import RestRoutes


def _format_ref(url, ref):
    pass


def _format_pref(url, pref):
    pass


class ClientV2Router:
    """Builds urls for v2"""

    def __init__(self, root_url):
        self.root_url = root_url
        self.base_url = "{}/v2/".format(root_url)
        self.routes = RestRoutes()

    def ping(self):
        # FIXME: The v2 ping is not returning capabilities
        pass

    def search(self, pattern, ignorecase):
        """URL search recipes"""
        pass

    def search_packages(self, ref, list_only):
        """URL search packages for a recipe"""
        pass

    def common_authenticate(self):
        pass

    def common_check_credentials(self):
        pass

    def recipe_file(self, ref, path):
        """Recipe file url"""
        pass

    def package_file(self, pref, path):
        """Package file url"""
        pass

    def remove_recipe(self, ref):
        """Remove recipe url"""
        pass

    def recipe_revisions(self, ref):
        """Get revisions for a recipe url"""
        pass

    def remove_package(self, pref):
        """Remove package url"""
        pass

    def remove_all_packages(self, ref):
        """Remove package url"""
        pass

    def recipe_snapshot(self, ref):
        """get recipe manifest url"""
        pass

    def package_snapshot(self, pref):
        """get recipe manifest url"""
        pass

    def package_revisions(self, pref):
        """get revisions for a package url"""
        pass

    def package_latest(self, pref):
        """Get the latest of a package"""
        pass

    def recipe_latest(self, ref):
        """Get the latest of a recipe"""
        pass

    def _for_package_file(self, pref, path):
        """url for getting a file from a package, with revisions"""
        pass

    def _for_package_files(self, pref):
        """url for getting the recipe list"""
        pass

    def _for_recipe_file(self, ref, path):
        """url for a recipe file, with or without revisions"""
        pass

    def _for_recipe_files(self, ref):
        """url for getting the recipe list"""
        pass

    def _for_recipe(self, ref):
        """url for a recipe with or without revisions (without rev,
        only for delete the root recipe, or v1)"""
        pass

    def _for_packages(self, ref):
        """url for a recipe with or without revisions"""
        pass

    def _for_package(self, pref):
        """url for the package with or without revisions"""
        pass

    @staticmethod
    def _format_ref_path(url, ref, path):
        pass

    @staticmethod
    def _format_pref_path(url, pref, path):
        pass
