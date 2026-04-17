import sqlite3

from conan.internal.cache.db.table import BaseDbTable
from conan.internal.errors import ConanReferenceDoesNotExistInDB, ConanReferenceAlreadyExistsInDB
from conan.api.model import RecipeReference
from conan.internal.util.dates import timestamp_now


class RecipesDBTable(BaseDbTable):
    table_name = 'recipes'
    columns_description = [('reference', str),
                           ('rrev', str),
                           ('path', str, False, True),
                           ('timestamp', float),
                           ('lru', int)]
    unique_together = ('reference', 'rrev')

    @staticmethod
    def _as_dict(row):
        pass

    def _where_clause(self, ref):
        pass

    def create(self, path, ref: RecipeReference):
        pass

    def update_timestamp(self, ref: RecipeReference):
        pass

    def remove(self, ref: RecipeReference):
        pass

    # returns all different conan references (name/version@user/channel)
    def all_references(self):
        pass

    def get_recipe(self, ref: RecipeReference):
        pass

    def get_latest_recipe(self, ref: RecipeReference):
        pass

    def get_recipe_revisions_references(self, ref: RecipeReference):
        pass

    def path_to_ref(self, path):
        pass
