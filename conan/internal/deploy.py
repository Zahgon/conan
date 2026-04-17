import filecmp
import os
import shutil
import fnmatch

from conan.internal.cache.home_paths import HomePaths
from conan.api.output import ConanOutput
from conan.internal.loader import load_python_file
from conan.internal.errors import conanfile_exception_formatter
from conan.errors import ConanException
from conan.internal.util.files import rmdir, mkdir, save


def _find_deployer(d, cache_deploy_folder):
    """ Implements the logic of finding a deployer, with priority:
    - 1) absolute paths
    - 2) relative to cwd
    - 3) in the cache/extensions/deploy folder
    - 4) built-in
    """
    pass


def do_deploys(home_folder, graph, deploy, deploy_package, deploy_folder):
    pass


def full_deploy(graph, output_folder):
    """
    Deploys to output_folder + host/dep/0.1/Release/x86_64 subfolder
    """
    pass


def runtime_deploy(graph, output_folder):
    """
    Deploy all the shared libraries and the executables of the dependencies in a flat directory.

    It preserves symlinks in case the configuration tools.deployer:symlinks is True.
    It preserves the directory structure when having subfolders
    """
    pass


def cyclonedx_1_4(graph, output_folder):
    pass


def cyclonedx_1_6(graph, output_folder):
    pass


def _flatten_directory(dep, src_dir, output_dir, symlinks, extension_filter=None):
    """
    Copy all the files from the source directory in a flat output directory, respecting subfolders.
    An optional string, named extension_filter, can be set to copy only the files with
    the listed extensions.
    """
    pass


def _deploy_single(dep, conanfile, output_folder, folder_name):
    pass


def direct_deploy(graph, output_folder):
    """
    Deploys to output_folder a single package,
    """
    pass
