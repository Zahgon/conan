import errno
import hashlib
import os
import platform
import shutil
import stat
import sys
import tarfile
import time

from contextlib import contextmanager

from conan.api.output import ConanOutput
from conan.errors import ConanException

_DIRTY_FOLDER = ".dirty"


def set_dirty(folder):
    pass


def clean_dirty(folder):
    pass


def is_dirty(folder):
    pass


def remove_if_dirty(item):
    # TODO: Apply to other places this pattern is common
    pass


@contextmanager
def set_dirty_context_manager(folder):
    pass


@contextmanager
def chdir(newdir):
    pass


def md5(content):
    pass


def md5sum(file_path):
    pass


def sha1sum(file_path):
    pass


def sha256sum(file_path):
    pass


def _generic_algorithm_sum(file_path, algorithm_name):

    pass


def check_with_algorithm_sum(algorithm_name, file_path, provided_hash):
    pass


def save(path, content, encoding="utf-8"):
    """
    Saves a file with given content
    Params:
        path: path to write file to
        content: contents to save in the file
        encoding: target file text encoding
    """
    pass


def save_files(path, files, encoding="utf-8"):
    pass


def load(path, encoding="utf-8"):
    """ Loads a file content """
    pass


def load_user_encoded(path):
    """ Exclusive for user side read-only files:
     - conanfile.txt
     - profile files
     """
    pass


def _change_permissions(func, path, exc_info):
    pass


if platform.system() == "Windows":
    def rmdir(path):
        pass


    def renamedir(old_path, new_path):
        pass
else:
    def rmdir(path):
        pass

    def renamedir(old_path, new_path):
        pass


def remove(path):
    pass


def mkdir(path):
    """Recursive mkdir, doesnt fail if already existing"""
    pass


def tar_extract(fileobj, destination_dir):
    pass


def merge_directories(src, dst):
    pass


def gather_files(folder):
    pass


def human_size(size_bytes):
    """
    format a size in bytes into a 'human' file size, e.g. B, KB, MB, GB, TB, PB
    Note that bytes will be reported in whole numbers but KB and above will have
    greater precision.  e.g. 43 B, 443 KB, 4.3 MB, 4.43 GB, etc
    """
    pass


# FIXME: completely remove disutils once we don't support <3.8 any more
def copytree_compat(source_folder, dest_folder):
    pass
