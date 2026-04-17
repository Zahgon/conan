from collections import OrderedDict

from conan.internal.errors import conanfile_remove_attr, conanfile_exception_formatter
from conan.errors import ConanException, ConanInvalidConfiguration
from conan.internal.methods import auto_header_only_package_id
from conan.internal.model.info import (ConanInfo, RequirementsInfo, RequirementInfo,
                                       PythonRequiresInfo)
from conan.internal.model.pkg_type import PackageType


def compute_package_id(node, modes, config_version, hook_manager):
    """
    Compute the binary package ID of this node
    """
    pass


def run_validate_package_id(conanfile, hook_manager):
    # IMPORTANT: This validation code must run before calling info.package_id(), to mark "invalid"
    pass
