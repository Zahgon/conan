import os
import sqlite3
from contextlib import contextmanager
from sqlite3 import OperationalError

from conan.errors import ConanException
from conan.internal.api.remotes import encrypt

REMOTES_USER_TABLE = "users_remotes"
LOCALDB = ".conan.db"

_localdb_encryption_key = os.environ.pop('CONAN_LOGIN_ENCRYPTION_KEY', None)


class LocalDB:

    def __init__(self, dbfolder):
        self.dbfile = os.path.join(dbfolder, LOCALDB)
        self.encryption_key = _localdb_encryption_key

        # Create the database file if it doesn't exist
        if not os.path.exists(self.dbfile):
            par = os.path.dirname(self.dbfile)
            os.makedirs(par, exist_ok=True)
            open(self.dbfile, 'w').close()

            with self._connect() as connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("create table if not exists %s "
                                   "(remote_url TEXT UNIQUE, user TEXT, "
                                   "token TEXT, refresh_token TEXT)" % REMOTES_USER_TABLE)
                except Exception as e:
                    message = f"Could not initialize local sqlite database {self.dbfile}"
                    raise ConanException(message, e)

    def _encode(self, value):
        pass

    def _decode(self, value):
        pass

    def clean(self, remote_url=None):
        pass

    @contextmanager
    def _connect(self):
        pass

    def get_login(self, remote_url):
        """ Returns login credentials. This method is also in charge of expiring them. """
        pass

    def get_username(self, remote_url):
        pass

    def store(self, user, token, refresh_token, remote_url):
        """ Login is a tuple of (user, token) """
        pass
