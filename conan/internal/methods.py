import os

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.errors import conanfile_exception_formatter, conanfile_remove_attr
from conan.internal.paths import CONANINFO
from conan.internal.model.manifest import FileTreeManifest
from conan.api.model import PkgReference
from conan.internal.model.pkg_type import PackageType
from conan.internal.model.requires import BuildRequirements, TestRequirements, ToolRequirements
from conan.internal.util.files import mkdir, chdir, save


def run_source_method(conanfile, hook_manager):
    pass


def run_build_method(conanfile, hook_manager):
    pass


def run_package_method(conanfile, package_id, hook_manager, ref):
    """ calls the recipe "package()" method
    - Assigns folders to conanfile.package_folder, source_folder, install_folder, build_folder
    - Calls pre-post package hook
    """
    pass


def run_configure_method(conanfile, down_options, profile_options, ref):
    """ Run all the config-related functions for the given conanfile object """
    pass


def auto_shared_fpic_config_options(conanfile):
    pass


def auto_shared_fpic_configure(conanfile):
    pass


def auto_header_only_package_id(conanfile):
    pass


def auto_language(conanfile):
    pass
