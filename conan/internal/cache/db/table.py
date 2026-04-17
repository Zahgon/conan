import sqlite3
import threading
import traceback
from collections import defaultdict, namedtuple
from contextlib import contextmanager
from typing import Tuple, List

from conan.api.output import ConanOutput
from conan.errors import ConanException


class BaseDbTable:
    table_name: str = None
    columns_description: List[Tuple[str, type]] = None
    row_type: namedtuple = None
    columns: namedtuple = None
    unique_together: tuple = None
    _lock: threading.Lock = None
    _lock_storage = defaultdict(threading.Lock)

    def __init__(self, filename):
        self.filename = filename
        column_names: List[str] = [it[0] for it in self.columns_description]
        self.row_type = namedtuple('_', column_names)
        self.columns = self.row_type(*column_names)
        self._lock = self._lock_storage[self.filename]

    @contextmanager
    def db_connection(self):
        pass

    def create_table(self):
        pass
