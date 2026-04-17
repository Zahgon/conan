import logging
import os
import shutil

import patch_ng
import yaml

from conan.errors import ConanException
from conan.internal.paths import DATA_YML
from conan.internal.util.files import mkdir, load, save


class PatchLogHandler(logging.Handler):
    def __init__(self, scoped_output, patch_file):
        logging.Handler.__init__(self, logging.DEBUG)
        self._scoped_output = scoped_output
        self.patchname = patch_file or "patch_ng"

    def emit(self, record):
        pass


def patch(conanfile, base_path=None, patch_file=None, patch_string=None, strip=0, fuzz=False, **kwargs):
    """
    Applies a diff from file (patch_file) or string (patch_string) in the conanfile.source_folder
    directory. The folder containing the sources can be customized with the self.folders attribute
    in the layout(self) method.

    :param conanfile: the current recipe, always pass 'self'
    :param base_path: The path is a relative path to conanfile.export_sources_folder unless an
           absolute path is provided.
    :param patch_file: Patch file that should be applied. The path is relative to the
           conanfile.source_folder unless an absolute path is provided.
    :param patch_string: Patch string that should be applied.
    :param strip: Number of folders to be stripped from the path.
    :param fuzz: Should accept fuzzy patches.
    :param kwargs: Extra parameters that can be added and will contribute to output information
    """
    pass


def apply_conandata_patches(conanfile):
    """
    Applies patches stored in ``conanfile.conan_data`` (read from ``conandata.yml`` file).
    It will apply all the patches under ``patches`` entry that matches the given
    ``conanfile.version``. If versions are not defined in ``conandata.yml`` it will apply all the
    patches directly under ``patches`` keyword.

    The key entries will be passed as kwargs to the ``patch`` function.
    """
    pass


def export_conandata_patches(conanfile):
    """
    Exports patches stored in 'conanfile.conan_data' (read from 'conandata.yml' file). It will export
    all the patches under 'patches' entry that matches the given 'conanfile.version'. If versions are
    not defined in 'conandata.yml' it will export all the patches directly under 'patches' keyword.
    """
    pass
