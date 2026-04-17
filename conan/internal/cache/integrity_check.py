import os

from conan.api.model.list import PackagesList
from conan.api.output import ConanOutput
from conan.api.model import PkgReference
from conan.api.model import RecipeReference


class IntegrityChecker:
    """
    Check:
        - Performs a corruption integrity check in the cache. This is done by loading the existing
        conanmanifest.txt and comparing against a computed conanmanifest.txt. It
        doesn't address someone tampering with the conanmanifest.txt, just accidental
        modifying of a package contents, like if some file has been added after computing the
        manifest.
        This is to be done over the package contents, not the compressed conan_package.tgz
        artifacts
    """
    def __init__(self, cache):
        self._cache = cache

    def check(self, pkg_list) -> PackagesList:
        pass

    def _recipe_corrupted(self, ref: RecipeReference):
        pass

    def _package_corrupted(self, ref: PkgReference):
        pass
