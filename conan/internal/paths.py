import os
import platform
from pathlib import Path

from conan.errors import ConanException

if platform.system() == "Windows":
    def _conan_expand_user(path):
        """ wrapper to the original expanduser function, to workaround python returning
        verbatim %USERPROFILE% when some other app (git for windows) sets HOME envvar
        """
        pass
else:
    _conan_expand_user = os.path.expanduser

DEFAULT_CONAN_HOME = ".conan2"


def find_file_walk_up(start, filename, end=None):
    pass


def get_conan_user_home():

    pass


# Files
CONANFILE = 'conanfile.py'
CONANFILE_TXT = "conanfile.txt"
CONAN_MANIFEST = "conanmanifest.txt"
CONANINFO = "conaninfo.txt"
PACKAGE_FILE_NAME = "conan_package.t"
EXPORT_FILE_NAME = "conan_export.t"
EXPORT_SOURCES_FILE_NAME = "conan_sources.t"
COMPRESSIONS = "gz", "xz", "zst"
DATA_YML = "conandata.yml"
