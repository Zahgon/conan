import os
import shutil

from conan.tools.files import copy
from conan.api.output import ConanOutput
from conan.tools.scm import Git
from conan.internal.errors import conanfile_exception_formatter
from conan.errors import ConanException
from conan.internal.model.manifest import FileTreeManifest
from conan.api.model import RecipeReference
from conan.internal.paths import DATA_YML
from conan.internal.util.files import is_dirty, rmdir, set_dirty, mkdir, clean_dirty, chdir


def cmd_export(loader, cache, hook_manager, global_conf, conanfile_path,
               name, version, user, channel,
               graph_lock=None, remotes=None):
    """ Export the recipe
    param conanfile_path: the original source directory of the user containing a
                       conanfile.py
    """
    pass


def _calc_revision(scoped_output, path, manifest, revision_mode, conanfile):
    pass


def _classify_patterns(patterns):
    pass


def _export_source(conanfile, destination_source_folder):
    pass


def _export_recipe(conanfile, destination_folder):
    pass


def _run_method(conanfile, method):
    pass
