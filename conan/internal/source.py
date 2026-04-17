import os

from conan.api.output import ConanOutput
from conan.internal.methods import run_source_method
from conan.tools.env import VirtualBuildEnv
from conan.internal.errors import NotFoundException
from conan.errors import ConanException
from conan.internal.util.files import is_dirty, mkdir, rmdir, set_dirty_context_manager, merge_directories, clean_dirty


def _try_get_sources(ref, remote_manager, recipe_layout, remote):
    pass


def retrieve_exports_sources(remote_manager, recipe_layout, conanfile, ref, remotes):
    """ the "exports_sources" sources are not retrieved unless necessary to build. In some
    occassions, conan needs to get them too, like if uploading to a server, to keep the recipes
    complete
    """
    pass


def config_source(export_source_folder, conanfile, hook_manager):
    """ Implements the sources configuration when a package is going to be built in the
    local cache:
    - remove old sources if dirty
    - do a copy of the exports_sources folders to the source folder in the cache
    - run the source() recipe method
    """
    pass
