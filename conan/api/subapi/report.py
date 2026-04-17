import base64
import os
from io import StringIO

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.api.model import RecipeReference
from conan.internal.errors import conanfile_exception_formatter
from conan.internal.graph.graph import CONTEXT_HOST
from conan.internal.graph.profile_node_definer import initialize_conanfile_profile
from conan.internal.source import config_source
from conan.internal.util.runners import conan_run


class ReportAPI:
    """ Used to compute the differences (the "diff") between two versions or revisions, for
    both the recipe and source code.
    """
    def __init__(self, conan_api, helpers):
        self._conan_api = conan_api
        self._helpers = helpers

    def diff(self, old_reference, new_reference, remotes, old_path=None, new_path=None, cwd=None):
        """
        Compare two recipes and return the differences.

        :param old_reference: The reference of the old recipe.
        :param new_reference: The reference of the new recipe.
        :param remotes: List of remotes to search for the recipes.
        :param old_path: Optional path to the old recipe's conanfile.py.
        :param new_path: Optional path to the new recipe's conanfile.py.
        :param cwd: Current working directory, used to resolve paths.
        :return: A dictionary with the differences between the two recipes.
        """
        pass


def _configure_source(conan_api, hook_manager, conanfile_path, ref, remotes):
    pass


def _get_ref_from_cache_or_remote(conan_api, reference, enabled_remotes):
    pass


def _export_recipe_from_path(conan_api, path_to_conanfile, reference, enabled_remotes, cwd=None):
    pass
