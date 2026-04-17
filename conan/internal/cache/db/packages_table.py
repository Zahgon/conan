import sqlite3

from conan.internal.cache.db.table import BaseDbTable
from conan.internal.errors import ConanReferenceDoesNotExistInDB, ConanReferenceAlreadyExistsInDB
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.dates import timestamp_now


class PackagesDBTable(BaseDbTable):
    table_name = 'packages'
    columns_description = [('reference', str),
                           ('rrev', str),
                           ('pkgid', str, True),
                           ('prev', str, True),
                           ('path', str, False, True),
                           ('timestamp', float),
                           ('build_id', str, True),
                           ('lru', int)]
    unique_together = ('reference', 'rrev', 'pkgid', 'prev')

    @staticmethod
    def _as_dict(row):
        pass

    def _where_clause(self, pref: PkgReference):
        pass

    def _set_clause(self, pref: PkgReference, path=None, build_id=None):
        pass

    def get(self, pref: PkgReference):
        """ Returns the row matching the reference or fails """
        where_clause = self._where_clause(pref)
        query = f'SELECT * FROM {self.table_name} ' \
                f'WHERE {where_clause};'

        with self.db_connection() as conn:
            r = conn.execute(query)
            row = r.fetchone()

        if not row:
            raise ConanReferenceDoesNotExistInDB(f"No entry for package '{repr(pref)}'")
        return self._as_dict(self.row_type(*row))

    def create(self, path, pref: PkgReference, build_id):
        pass

    def update_timestamp(self, pref: PkgReference, path: str, build_id: str):
        pass

    def remove_build_id(self, pref):
        pass

    def remove_recipe(self, ref: RecipeReference):
        # can't use the _where_clause, because that is an exact match on the package_id, etc
        pass

    def remove(self, pref: PkgReference):
        pass

    def get_package_revisions_references(self, pref: PkgReference, only_latest_prev=False):
        pass

    def get_package_revisions_reference_exists(self, pref: PkgReference):
        pass

    def get_package_references(self, ref: RecipeReference, only_latest_prev=True):
        # Return the latest revisions
        pass

    def get_package_references_with_build_id_match(self, ref: RecipeReference, build_id):
        # Return the latest revisions
        pass

    def path_to_ref(self, path):
        pass
