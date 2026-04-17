import os

from conan.internal.loader import load_python_file
from conan.errors import ConanException, ConanInvalidConfiguration

valid_hook_methods = ["pre_export", "post_export",
                      "pre_validate", "post_validate",
                      "pre_source", "post_source",
                      "pre_generate", "post_generate",
                      "pre_build", "post_build", "post_build_fail",
                      "pre_package", "post_package",
                      "pre_package_info", "post_package_info",
                      "post_package_id"]  # package_id is called a lot more than others, only post


class HookManager:

    def __init__(self, hooks_folder):
        self._hooks_folder = hooks_folder
        self.hooks = {}
        self.validate_hook = False  # Quick check for performance
        self.post_package_id_hook = False  # Quick check for performance
        self._load_hooks()  # A bit dirty, but avoid breaking tests

    def execute(self, method_name, conanfile):
        pass

    def _load_hooks(self):
        pass

    def _load_hook(self, hook_path, hook_name):
        pass

    def reinit(self):
        pass
