import calendar
import datetime
import time

from dateutil import parser


def from_timestamp_to_iso8601(timestamp):
    # Used exclusively by conan_server to return the date in iso format (same as artifactory)
    pass


def _from_iso8601_to_datetime(iso_str):
    pass


def from_iso8601_to_timestamp(iso_str):
    # used by RestClient v2 to transform from HTTP API (iso) to Conan internal timestamp
    pass


def timestamp_now():
    # seconds since epoch 0, easy to store, in UTC
    # Used in Manifest timestamp, in packagesDB LRU and in timestamp of backup-sources json
    pass


def revision_timestamp_now():
    pass


def timestamp_to_str(timestamp):
    # used by ref.repr_humantime() to print human readable time
    pass
