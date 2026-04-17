import os
import textwrap
from collections import OrderedDict

from jinja2 import Template

from conan.api.output import ConanOutput
from conan.internal import check_duplicated_generator
from conan.tools.build import use_win_mingw
from conan.tools.cmake.presets import write_cmake_presets
from conan.tools.cmake.toolchain import CONAN_TOOLCHAIN_FILENAME
from conan.tools.cmake.toolchain.blocks import (ExtraVariablesBlock, ToolchainBlocks,
                                                UserToolchain, GenericSystemBlock,
                                                AndroidSystemBlock, AppleSystemBlock, FPicBlock,
                                                ArchitectureBlock, GLibCXXBlock, VSRuntimeBlock,
                                                CppStdBlock, ParallelBlock, CMakeFlagsInitBlock,
                                                TryCompileBlock, FindFiles, PkgConfigBlock,
                                                SkipRPath, SharedLibBock, OutputDirsBlock,
                                                ExtraFlagsBlock, CompilersBlock, LinkerScriptsBlock,
                                                VSDebuggerEnvironment, VariablesBlock,
                                                PreprocessorBlock, RpathLinkFlagsBlock)
from conan.tools.cmake.utils import is_multi_configuration
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.intel import IntelCC
from conan.tools.microsoft import VCVars
from conan.tools.microsoft.visual import vs_ide_version
from conan.errors import ConanException
from conan.internal.model.options import _PackageOption
from conan.internal.graph.graph import RECIPE_CONSUMER, RECIPE_EDITABLE
from conan.internal.util.files import save


class Variables(OrderedDict):
    _configuration_types = None  # Needed for py27 to avoid infinite recursion

    def __init__(self):
        super(Variables, self).__init__()
        self._configuration_types = {}

    def __getattribute__(self, config):
        try:
            return super(Variables, self).__getattribute__(config)
        except AttributeError:
            return self._configuration_types.setdefault(config, OrderedDict())

    @property
    def configuration_types(self):
        # Reverse index for the configuration_types variables
        pass

    def quote_preprocessor_strings(self):
        pass


class CMakeToolchain:

    filename = CONAN_TOOLCHAIN_FILENAME

    _template = textwrap.dedent("""\
        # Conan automatically generated toolchain file
        # DO NOT EDIT MANUALLY, it will be overwritten

        # Avoid including toolchain file several times (bad if appending to variables like
        #   CMAKE_CXX_FLAGS. See https://github.com/android/ndk/issues/323
        include_guard()
        message(STATUS "Using Conan toolchain: ${CMAKE_CURRENT_LIST_FILE}")
        if(${CMAKE_VERSION} VERSION_LESS "3.15")
            message(FATAL_ERROR "The 'CMakeToolchain' generator only works with CMake >= 3.15")
        endif()

        {% for conan_block in conan_blocks %}
        {{ conan_block }}
        {% endfor %}

        if(CMAKE_POLICY_DEFAULT_CMP0091)  # Avoid unused and not-initialized warnings
        endif()
        """)

    def __init__(self, conanfile, generator=None):
        self._conanfile = conanfile
        self.generator = self._get_generator(generator)
        self.variables = Variables()
        # This doesn't support multi-config, they go to the same configPreset common in multi-config
        self.cache_variables = {}
        self.preprocessor_definitions = Variables()

        self.extra_cxxflags = []
        self.extra_cflags = []
        self.extra_sharedlinkflags = []
        self.extra_exelinkflags = []
        self.add_rpath_link = False

        self.blocks = ToolchainBlocks(self._conanfile, self,
                                      [("user_toolchain", UserToolchain),
                                       ("generic_system", GenericSystemBlock),
                                       ("compilers", CompilersBlock),
                                       ("android_system", AndroidSystemBlock),
                                       ("apple_system", AppleSystemBlock),
                                       ("fpic", FPicBlock),
                                       ("arch_flags", ArchitectureBlock),
                                       ("linker_scripts", LinkerScriptsBlock),
                                       ("rpath_link_flags", RpathLinkFlagsBlock),
                                       ("libcxx", GLibCXXBlock),
                                       ("vs_runtime", VSRuntimeBlock),
                                       ("vs_debugger_environment", VSDebuggerEnvironment),
                                       ("cppstd", CppStdBlock),
                                       ("parallel", ParallelBlock),
                                       ("extra_flags", ExtraFlagsBlock),
                                       ("cmake_flags_init", CMakeFlagsInitBlock),
                                       ("extra_variables", ExtraVariablesBlock),
                                       ("try_compile", TryCompileBlock),
                                       ("find_paths", FindFiles),
                                       ("pkg_config", PkgConfigBlock),
                                       ("rpath", SkipRPath),
                                       ("shared", SharedLibBock),
                                       ("output_dirs", OutputDirsBlock),
                                       ("variables", VariablesBlock),
                                       ("preprocessor", PreprocessorBlock)])

        # Set the CMAKE_MODULE_PATH and CMAKE_PREFIX_PATH to the deps .builddirs
        self.find_builddirs = True
        self.user_presets_path = "CMakeUserPresets.json"
        self.presets_prefix = "conan"
        self.presets_build_environment = None
        self.presets_run_environment = None
        self.absolute_paths = False  # By default use relative paths to toolchain and presets

    def _context(self):
        """ Returns dict, the context for the template
        """
        pass

    @property
    def content(self):
        pass

    @property
    def is_multi_configuration(self):
        pass

    def _find_cmake_exe(self):
        pass

    def generate(self):
        """
          This method will save the generated files to the conanfile.generators_folder
        """
        pass

    def _get_generator(self, recipe_generator):
        # Returns the name of the generator to be used by CMake
        pass
