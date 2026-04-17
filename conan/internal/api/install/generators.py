import importlib
import inspect
import os
import traceback

from conan.errors import ConanException
from conan.internal.cache.home_paths import HomePaths
from conan.internal.errors import conanfile_exception_formatter
from conan.internal.util.files import mkdir, chdir


_generators = {"CMakeToolchain": "conan.tools.cmake",
               "CMakeDeps": "conan.tools.cmake",
               "CMakeConfigDeps": "conan.tools.cmake",
               "MesonToolchain": "conan.tools.meson",
               "MSBuildDeps": "conan.tools.microsoft",
               "MSBuildToolchain": "conan.tools.microsoft",
               "NMakeToolchain": "conan.tools.microsoft",
               "NMakeDeps": "conan.tools.microsoft",
               "VCVars": "conan.tools.microsoft",
               "VirtualRunEnv": "conan.tools.env.virtualrunenv",
               "VirtualBuildEnv": "conan.tools.env.virtualbuildenv",
               "AutotoolsDeps": "conan.tools.gnu",
               "AutotoolsToolchain": "conan.tools.gnu",
               "GnuToolchain": "conan.tools.gnu",
               "PkgConfigDeps": "conan.tools.gnu",
               "BazelDeps": "conan.tools.google",
               "BazelToolchain": "conan.tools.google",
               "IntelCC": "conan.tools.intel",
               "XcodeDeps": "conan.tools.apple",
               "XcodeToolchain": "conan.tools.apple",
               "PremakeDeps": "conan.tools.premake",
               "PremakeToolchain": "conan.tools.premake",
               "MakeDeps": "conan.tools.gnu",
               "SConsDeps": "conan.tools.scons",
               "QbsDeps": "conan.tools.qbs",
               "QbsProfile": "conan.tools.qbs",
               "CPSDeps": "conan.tools.cps",
               "ROSEnv": "conan.tools.ros"
               }


def _get_generator_class(generator_name):
    pass


def load_cache_generators(path):
    pass


def write_generators(conanfile, hook_manager, home_folder, envs_generation=None):
    pass


def _receive_conf(conanfile):
    """  collect conf_info from the immediate build_requires, aggregate it and injects/update
    current conf
    """
    pass


def _receive_generators(conanfile):
    """  Collect generators_info from the immediate build_requires"""
    pass


def relativize_path(path, conanfile, placeholder, normalize=True):
    """
    relative path from the "generators_folder" to "path", asuming the root file, like
    conan_toolchain.cmake will be directly in the "generators_folder"
    """
    pass
