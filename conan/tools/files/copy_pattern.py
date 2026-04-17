import filecmp
import fnmatch
import os
import shutil

from conan.errors import ConanException
from conan.internal.util.files import mkdir


def copy(conanfile, pattern, src, dst, keep_path=True, excludes=None,
         ignore_case=True, overwrite_equal=False):
    """
    Copy the files matching the pattern (fnmatch) at the src folder to a dst folder.

    :param conanfile: The current recipe object. Always use ``self``.
    :param pattern: (Required) An fnmatch file pattern of the files that should be copied.
           It must not start with ``..`` relative path or an exception will be raised.
    :param src: (Required) Source folder in which those files will be searched. This folder
           will be stripped from the dst parameter. E.g., lib/Debug/x86.
    :param dst: (Required) Destination local folder. It must be different from src value or an
           exception will be raised.
    :param keep_path: (Optional, defaulted to ``True``) Means if you want to keep the relative
           path when you copy the files from the src folder to the dst one.
    :param excludes: (Optional, defaulted to ``None``) A tuple/list of fnmatch patterns or even a
           single one to be excluded from the copy.
    :param ignore_case: (Optional, defaulted to ``True``) If enabled, it will do a
           case-insensitive pattern matching. will do a case-insensitive pattern matching when
           ``True``
    :param overwrite_equal: (Optional, default ``False``). If the file to be copied already exists
           in the destination folder, only really copy it if it seems different (different size,
           different modification time)
    :return: list of copied files
    """
    pass


def _filter_files(src, pattern, excludes, ignore_case, excluded_folder):
    """ return a list of the files matching the patterns
    The list will be relative path names wrt to the root src folder
    """
    pass


def _copy_files(files, src, dst, keep_path, overwrite_equal):
    """ executes a multiple file copy from [(src_file, dst_file), (..)]
    managing symlinks if necessary
    """
    pass


def _copy_files_symlinked_to_folders(files_symlinked_to_folders, src, dst):
    """Copy the files that are symlinks to folders from src to dst.
       The files are already filtered with the specified pattern"""
    pass
