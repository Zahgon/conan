import json
import os
import platform
import textwrap

from conan.api.output import ConanOutput, Color
from conan.tools.cmake.layout import get_build_folder_custom_vars
from conan.tools.cmake.toolchain.blocks import GenericSystemBlock
from conan.tools.cmake.utils import is_multi_configuration
from conan.tools.build import build_jobs
from conan.tools.microsoft import is_msvc
from conan.internal.graph.graph import RECIPE_CONSUMER
from conan.errors import ConanException
from conan.internal.util.files import save, load


def write_cmake_presets(conanfile, toolchain_file, generator, cache_variables,
                        user_presets_path=None, preset_prefix=None, buildenv=None, runenv=None,
                        cmake_executable=None, absolute_paths=None):
    pass


class _CMakePresets:
    """ Conan generated main CMakePresets.json inside the generators_folder
    """
    @staticmethod
    def generate(conanfile, toolchain_file, generator, cache_variables, preset_prefix, buildenv,
                 runenv, cmake_executable, absolute_paths):
        pass

    @staticmethod
    def _insert_preset(data, preset_type, preset):
        pass

    @staticmethod
    def _contents(conanfile, toolchain_file, cache_variables, generator, preset_prefix, buildenv,
                  runenv, cmake_executable):
        """
        Contents for the CMakePresets.json
        It uses schema version 3 unless it is forced to 2
        """
        pass

    @staticmethod
    def _configure_preset(conanfile, generator, cache_variables, toolchain_file, multiconfig,
                          preset_prefix, buildenv, cmake_executable):
        pass

    @staticmethod
    def _common_preset_fields(conanfile, multiconfig, preset_prefix):
        pass

    @staticmethod
    def _build_preset_fields(conanfile, multiconfig, preset_prefix):
        pass

    @staticmethod
    def _test_preset_fields(conanfile, multiconfig, preset_prefix, runenv):
        pass

    @staticmethod
    def _build_and_test_preset_name(conanfile):
        pass

    @staticmethod
    def _configure_preset_name(conanfile, multiconfig):
        pass


class _IncludingPresets:
    """
    CMakeUserPresets or ConanPresets.json that include the main generated CMakePresets
    """

    @staticmethod
    def generate(conanfile, preset_path, user_presets_path, preset_prefix, preset_data,
                 absolute_paths):
        pass

    @staticmethod
    def _update_stubs(data, inherited_user, output_dir, absolute_paths):
        """
        Set configurePresets/buildPresets/testPresets to stubs for conan-* presets
        that the user inherits but that don't have a real preset of the same type in the includes.
        """
        pass

    @staticmethod
    def _collect_user_inherits(output_dir, preset_prefix):
        # Collect all the existing targets in the user files, to create empty conan- presets
        # so things doesn't break for multi-platform, when inherits don't exist
        pass

    @staticmethod
    def _append_user_preset_path(data, preset_path, output_dir):
        """ - Appends a 'include' to preset_path if the schema supports it.
            - Otherwise it merges to "data" all the configurePresets, buildPresets etc from the
              read preset_path.
        """
        pass


def load_cmake_presets(folder):
    pass
