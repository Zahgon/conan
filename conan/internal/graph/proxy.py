from fnmatch import fnmatch

from conan.api.output import ConanOutput
from conan.internal.cache.conan_reference_layout import BasicLayout
from conan.internal.graph.graph import (RECIPE_DOWNLOADED, RECIPE_INCACHE, RECIPE_NEWER,
                                        RECIPE_NOT_IN_REMOTE, RECIPE_UPDATED, RECIPE_EDITABLE,
                                        RECIPE_INCACHE_DATE_UPDATED, RECIPE_UPDATEABLE)
from conan.internal.errors import NotFoundException, ConanReferenceAlreadyExistsInDB
from conan.errors import ConanException


class ConanProxy:
    def __init__(self, cache, remote_manager, editable_packages, legacy_update=None):
        # collaborators
        self._editable_packages = editable_packages
        self._cache = cache
        self._remote_manager = remote_manager
        self._resolved = {}  # Cache of the requested recipes to optimize calls
        self._legacy_update = legacy_update

    def get_recipe(self, ref, remotes, update, check_update):
        """
        :return: Tuple (layout, status, remote)
        """
        pass

    # return the remote where the recipe was found or None if the recipe was not found
    def _get_recipe(self, reference, remotes, update, check_update):
        pass

    def _find_newest_recipe_in_remotes(self, reference, remotes, update, check_update):
        pass

    def _download_recipe(self, ref, remotes, scoped_output, update, check_update):
        # When a recipe doesn't existin local cache, it is retrieved from servers
        pass

    def _download(self, ref, remote):
        pass


def should_update_reference(reference, update):
    pass
