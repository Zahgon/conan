import os
import re
import textwrap

from jinja2 import Template

from conan.internal.internal_tools import universal_arch_separator, is_universal_arch
from conan.tools.apple.apple import get_apple_sdk_fullname, _to_apple_arch
from conan.tools.android.utils import android_abi
from conan.tools.apple.apple import is_apple_os, to_apple_arch
from conan.tools.build import build_jobs
from conan.tools.build.flags import architecture_flag, architecture_link_flag, libcxx_flags, threads_flags
from conan.tools.build.cross_building import cross_building
from conan.tools.cmake.toolchain import CONAN_TOOLCHAIN_FILENAME
from conan.tools.cmake.utils import is_multi_configuration
from conan.tools.intel import IntelCC
from conan.tools.microsoft.visual import msvc_version_to_toolset_version, msvc_platform_from_arch
from conan.internal.api.install.generators import relativize_path
from conan.internal.subsystems import deduce_subsystem, WINDOWS
from conan.errors import ConanException
from conan.internal.model.version import Version
from conan.internal.util.files import load


class Block:
    def __init__(self, conanfile, toolchain, name):
        self._conanfile = conanfile
        self._toolchain = toolchain
        self._context_values = None
        self._name = name

    @property
    def values(self):
        pass

    @values.setter
    def values(self, context_values):
        pass

    def get_rendered_content(self):
        pass

    def context(self):
        pass

    @property
    def template(self):
        pass


class VSRuntimeBlock(Block):
    template = textwrap.dedent("""\
        # Definition of VS runtime CMAKE_MSVC_RUNTIME_LIBRARY, from settings build_type,
        # compiler.runtime, compiler.runtime_type

        {% set genexpr = namespace(str='') %}
        {% for config, value in vs_runtimes.items() %}
            {% set genexpr.str = genexpr.str +
                                  '$<$<CONFIG:' + config + '>:' + value|string + '>' %}
        {% endfor %}
        cmake_policy(GET CMP0091 POLICY_CMP0091)
        if(NOT "${POLICY_CMP0091}" STREQUAL NEW)
            message(FATAL_ERROR "The CMake policy CMP0091 must be NEW, but is '${POLICY_CMP0091}'")
        endif()
        message(STATUS "Conan toolchain: Setting CMAKE_MSVC_RUNTIME_LIBRARY={{ genexpr.str  }}")
        set(CMAKE_MSVC_RUNTIME_LIBRARY "{{ genexpr.str }}")
        """)

    def context(self):
        # Parsing existing toolchain file to get existing configured runtimes
        pass


class VSDebuggerEnvironment(Block):
    template = textwrap.dedent("""\
        # Definition of CMAKE_VS_DEBUGGER_ENVIRONMENT from "bindirs" folders of dependencies
        # for execution of applications with shared libraries within the VS IDE

        {% if vs_debugger_path %}
        # if the file exists it will be loaded by FindFiles block and the variable defined there
        if(NOT EXISTS "${CMAKE_CURRENT_LIST_DIR}/conan_cmakedeps_paths.cmake")
        # This variable requires CMake>=3.27 to work
        set(CMAKE_VS_DEBUGGER_ENVIRONMENT "{{ vs_debugger_path }}")
        endif()
        {% endif %}
        """)

    def context(self):
        pass


class FPicBlock(Block):
    template = textwrap.dedent("""\
        # Defining CMAKE_POSITION_INDEPENDENT_CODE for static libraries when necessary

        {% if fpic %}
        message(STATUS "Conan toolchain: Setting CMAKE_POSITION_INDEPENDENT_CODE={{ fpic }} (options.fPIC)")
        set(CMAKE_POSITION_INDEPENDENT_CODE {{ fpic }} CACHE BOOL "Position independent code")
        {% endif %}
        """)

    def context(self):
        pass


class GLibCXXBlock(Block):
    template = textwrap.dedent("""\
        # Definition of libcxx from 'compiler.libcxx' setting, defining the
        # right CXX_FLAGS for that libcxx

        {% if set_libcxx %}
        message(STATUS "Conan toolchain: Defining libcxx as C++ flags: {{ set_libcxx }}")
        string(APPEND CONAN_CXX_FLAGS " {{ set_libcxx }}")
        {% endif %}
        {% if glibcxx %}
        message(STATUS "Conan toolchain: Adding glibcxx compile definition: {{ glibcxx }}")
        add_compile_definitions({{ glibcxx }})
        {% endif %}
        """)

    def context(self):
        pass


class SkipRPath(Block):
    template = textwrap.dedent("""\
        # Defining CMAKE_SKIP_RPATH

        {% if skip_rpath %}
        set(CMAKE_SKIP_RPATH 1 CACHE BOOL "rpaths" FORCE)
        # Policy CMP0068
        # We want the old behavior, in CMake >= 3.9 CMAKE_SKIP_RPATH won't affect install_name in OSX
        set(CMAKE_INSTALL_NAME_DIR "")
        {% endif %}
        """)

    skip_rpath = False

    def context(self):
        pass


class ArchitectureBlock(Block):
    template = textwrap.dedent("""\
        {% if arch_flag %}
        # Define C++ flags, C flags and linker flags from 'settings.arch'
        message(STATUS "Conan toolchain: Defining architecture flag: {{ arch_flag }}")
        string(APPEND CONAN_CXX_FLAGS " {{ arch_flag }}")
        string(APPEND CONAN_C_FLAGS " {{ arch_flag }}")
        string(APPEND CONAN_SHARED_LINKER_FLAGS " {{ arch_flag }}")
        string(APPEND CONAN_EXE_LINKER_FLAGS " {{ arch_flag }}")
        {% endif %}
        {% if arch_link_flag %}
        message(STATUS "Conan toolchain: Defining architecture linker flag: {{ arch_link_flag }}")
        string(APPEND CONAN_SHARED_LINKER_FLAGS " {{ arch_link_flag }}")
        string(APPEND CONAN_EXE_LINKER_FLAGS " {{ arch_link_flag }}")
        {% endif %}
        {% if thread_flags_list %}
        # Define C++ flags, C flags and linker flags from 'compiler.threads'
        message(STATUS "Conan toolchain: Defining thread flags: {{ thread_flags_list }}")
        string(APPEND CONAN_CXX_FLAGS " {{ thread_flags_list }}")
        string(APPEND CONAN_C_FLAGS " {{ thread_flags_list }}")
        string(APPEND CONAN_SHARED_LINKER_FLAGS " {{ thread_flags_list }}")
        string(APPEND CONAN_EXE_LINKER_FLAGS " {{ thread_flags_list }}")
        {% endif %}
        """)

    def context(self):
        pass

class RpathLinkFlagsBlock(Block):
    template = textwrap.dedent("""\
        # Pass -rpath-link pointing to all directories with runtime libraries
        {% if rpath_link_flags %}
        string(APPEND CONAN_EXE_LINKER_FLAGS " {{ rpath_link_flags }}")
        string(APPEND CONAN_SHARED_LINKER_FLAGS " {{ rpath_link_flags }}")
        {% endif %}
        """)

    def context(self):
        pass

class LinkerScriptsBlock(Block):
    template = textwrap.dedent("""\
        # Add linker flags from tools.build:linker_scripts conf

        message(STATUS "Conan toolchain: Defining linker script flag: {{ linker_script_flags }}")
        string(APPEND CONAN_EXE_LINKER_FLAGS " {{ linker_script_flags }}")
        """)

    def context(self):
        pass


class CppStdBlock(Block):
    template = textwrap.dedent("""\
        # Define the C++ and C standards from 'compiler.cppstd' and 'compiler.cstd'

        function(conan_modify_std_watch variable access value current_list_file stack)
            set(conan_watched_std_variable "{{ cppstd }}")
            if (${variable} STREQUAL "CMAKE_C_STANDARD")
                set(conan_watched_std_variable "{{ cstd }}")
            endif()
            if ("${access}" STREQUAL "MODIFIED_ACCESS" AND NOT "${value}" STREQUAL "${conan_watched_std_variable}")
                message(STATUS "Warning: Standard ${variable} value defined in conan_toolchain.cmake to ${conan_watched_std_variable} has been modified to ${value} by ${current_list_file}")
            endif()
            unset(conan_watched_std_variable)
        endfunction()

        {% if cppstd %}
        message(STATUS "Conan toolchain: C++ Standard {{ cppstd }} with extensions {{ cppstd_extensions }}")
        set(CMAKE_CXX_STANDARD {{ cppstd }})
        set(CMAKE_CXX_EXTENSIONS {{ cppstd_extensions }})
        set(CMAKE_CXX_STANDARD_REQUIRED ON)
        variable_watch(CMAKE_CXX_STANDARD conan_modify_std_watch)
        {% endif %}
        {% if cstd %}
        message(STATUS "Conan toolchain: C Standard {{ cstd }} with extensions {{ cstd_extensions }}")
        set(CMAKE_C_STANDARD {{ cstd }})
        set(CMAKE_C_EXTENSIONS {{ cstd_extensions }})
        set(CMAKE_C_STANDARD_REQUIRED ON)
        variable_watch(CMAKE_C_STANDARD conan_modify_std_watch)
        {% endif %}
        """)

    def context(self):
        pass


class SharedLibBock(Block):
    template = textwrap.dedent("""\
        # Define BUILD_SHARED_LIBS for shared libraries

        message(STATUS "Conan toolchain: Setting BUILD_SHARED_LIBS = {{ shared_libs }}")
        set(BUILD_SHARED_LIBS {{ shared_libs }} CACHE BOOL "Build shared libraries")
        """)

    def context(self):
        pass


class ParallelBlock(Block):
    template = textwrap.dedent("""\
        # Define VS paralell build /MP flags

        string(APPEND CONAN_CXX_FLAGS " /MP{{ parallel }}")
        string(APPEND CONAN_C_FLAGS " /MP{{ parallel }}")
        """)

    def context(self):
        # TODO: Check this conf

        pass


class AndroidSystemBlock(Block):

    template = textwrap.dedent("""\
        # Define Android variables ANDROID_PLATFORM, ANDROID_STL, ANDROID_ABI, etc
        # and include(.../android.toolchain.cmake) from NDK toolchain file

        # New Android toolchain definitions
        message(STATUS "Conan toolchain: Setting Android platform: {{ android_platform }}")
        set(ANDROID_PLATFORM {{ android_platform }})
        {% if android_stl %}
        message(STATUS "Conan toolchain: Setting Android stl: {{ android_stl }}")
        set(ANDROID_STL {{ android_stl }})
        {% endif %}
        message(STATUS "Conan toolchain: Setting Android abi: {{ android_abi }}")
        set(ANDROID_ABI {{ android_abi }})
        {% if android_use_legacy_toolchain_file %}
        set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE {{ android_use_legacy_toolchain_file }})
        {% endif %}
        include("{{ android_ndk_path }}/build/cmake/android.toolchain.cmake")
        """)

    def context(self):
        pass


class AppleSystemBlock(Block):
    template = textwrap.dedent("""\
        # Define Apple architectures, sysroot, deployment target, bitcode, etc

        # Set the architectures for which to build.
        set(CMAKE_OSX_ARCHITECTURES {{ cmake_osx_architectures }} CACHE STRING "" FORCE)
        # Setting CMAKE_OSX_SYSROOT SDK, when using Xcode generator the name is enough
        # but full path is necessary for others
        set(CMAKE_OSX_SYSROOT {{ cmake_osx_sysroot }} CACHE STRING "" FORCE)
        {% if cmake_osx_deployment_target is defined %}
        # Setting CMAKE_OSX_DEPLOYMENT_TARGET if "os.version" is defined by the used conan profile
        set(CMAKE_OSX_DEPLOYMENT_TARGET "{{ cmake_osx_deployment_target }}" CACHE STRING "")
        {% endif %}
        set(BITCODE "")
        set(FOBJC_ARC "")
        set(VISIBILITY "")
        {% if enable_bitcode %}
        # Bitcode ON
        set(CMAKE_XCODE_ATTRIBUTE_ENABLE_BITCODE "YES")
        set(CMAKE_XCODE_ATTRIBUTE_BITCODE_GENERATION_MODE "bitcode")
        {% if enable_bitcode_marker %}
        set(BITCODE "-fembed-bitcode-marker")
        {% else %}
        set(BITCODE "-fembed-bitcode")
        {% endif %}
        {% elif enable_bitcode is not none %}
        # Bitcode OFF
        set(CMAKE_XCODE_ATTRIBUTE_ENABLE_BITCODE "NO")
        {% endif %}
        {% if enable_arc %}
        # ARC ON
        set(FOBJC_ARC "-fobjc-arc")
        set(CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC "YES")
        {% elif enable_arc is not none %}
        # ARC OFF
        set(FOBJC_ARC "-fno-objc-arc")
        set(CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC "NO")
        {% endif %}
        {% if enable_visibility %}
        # Visibility ON
        set(CMAKE_XCODE_ATTRIBUTE_GCC_SYMBOLS_PRIVATE_EXTERN "NO")
        set(VISIBILITY "-fvisibility=default")
        {% elif enable_visibility is not none %}
        # Visibility OFF
        set(VISIBILITY "-fvisibility=hidden -fvisibility-inlines-hidden")
        set(CMAKE_XCODE_ATTRIBUTE_GCC_SYMBOLS_PRIVATE_EXTERN "YES")
        {% endif %}
        #Check if Xcode generator is used, since that will handle these flags automagically
        if(CMAKE_GENERATOR MATCHES "Xcode")
          message(DEBUG "Not setting any manual command-line buildflags, since Xcode is selected as generator.")
        else()
            string(APPEND CONAN_C_FLAGS " ${BITCODE} ${VISIBILITY}")
            string(APPEND CONAN_CXX_FLAGS " ${BITCODE} ${VISIBILITY}")
            # Objective-C/C++ specific flags
            string(APPEND CONAN_OBJC_FLAGS " ${BITCODE} ${VISIBILITY} ${FOBJC_ARC}")
            string(APPEND CONAN_OBJCXX_FLAGS " ${BITCODE} ${VISIBILITY} ${FOBJC_ARC}")
        endif()
        """)

    def context(self):
        pass


class FindFiles(Block):
    template = textwrap.dedent("""\
        # Define paths to find packages, programs, libraries, etc.
        if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/conan_cmakedeps_paths.cmake")
          message(STATUS "Conan toolchain: Including CMakeConfigDeps generated conan_cmakedeps_paths.cmake")
          include("${CMAKE_CURRENT_LIST_DIR}/conan_cmakedeps_paths.cmake")
        else()

        {% if find_package_prefer_config %}
        set(CMAKE_FIND_PACKAGE_PREFER_CONFIG {{ find_package_prefer_config }})
        {% endif %}

        # Definition of CMAKE_MODULE_PATH
        {% if build_paths %}
        list(PREPEND CMAKE_MODULE_PATH {{ build_paths }})
        {% endif %}
        {% if generators_folder %}
        # the generators folder (where conan generates files, like this toolchain)
        list(PREPEND CMAKE_MODULE_PATH {{ generators_folder }})
        {% endif %}

        # Definition of CMAKE_PREFIX_PATH, CMAKE_XXXXX_PATH
        {% if build_paths %}
        # The explicitly defined "builddirs" of "host" context dependencies must be in PREFIX_PATH
        list(PREPEND CMAKE_PREFIX_PATH {{ build_paths }})
        {% endif %}
        {% if generators_folder %}
        # The Conan local "generators" folder, where this toolchain is saved.
        list(PREPEND CMAKE_PREFIX_PATH {{ generators_folder }} )
        {% endif %}
        {% if cmake_program_path %}
        list(PREPEND CMAKE_PROGRAM_PATH {{ cmake_program_path }})
        {% endif %}
        {% if cmake_library_path %}
        list(PREPEND CMAKE_LIBRARY_PATH {{ cmake_library_path }})
        {% endif %}
        {% if is_apple and cmake_framework_path %}
        list(PREPEND CMAKE_FRAMEWORK_PATH {{ cmake_framework_path }})
        {% endif %}
        {% if cmake_include_path %}
        list(PREPEND CMAKE_INCLUDE_PATH {{ cmake_include_path }})
        {% endif %}
        {% if host_runtime_dirs %}
        set(CONAN_RUNTIME_LIB_DIRS {{ host_runtime_dirs }} )
        {% endif %}

        {% if cross_building %}
        if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_PACKAGE OR CMAKE_FIND_ROOT_PATH_MODE_PACKAGE STREQUAL "ONLY")
            set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE "BOTH")
        endif()
        if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_PROGRAM OR CMAKE_FIND_ROOT_PATH_MODE_PROGRAM STREQUAL "ONLY")
            set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM "BOTH")
        endif()
        if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_LIBRARY OR CMAKE_FIND_ROOT_PATH_MODE_LIBRARY STREQUAL "ONLY")
            set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY "BOTH")
        endif()
        {% if is_apple %}
        if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_FRAMEWORK OR CMAKE_FIND_ROOT_PATH_MODE_FRAMEWORK STREQUAL "ONLY")
            set(CMAKE_FIND_ROOT_PATH_MODE_FRAMEWORK "BOTH")
        endif()
        {% endif %}
        if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_INCLUDE OR CMAKE_FIND_ROOT_PATH_MODE_INCLUDE STREQUAL "ONLY")
            set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE "BOTH")
        endif()
        {% endif %}
        endif()
    """)

    def _runtime_dirs_value(self, dirs):
        pass

    def _get_host_runtime_dirs(self, host_req):
        pass

    def _join_paths(self, paths):
        pass

    def context(self):
        # To find the generated cmake_find_package finders
        # TODO: Change this for parameterized output location of CMakeDeps
        pass


class PkgConfigBlock(Block):
    template = textwrap.dedent("""\
        # Define pkg-config from 'tools.gnu:pkg_config' executable and paths

        {% if pkg_config %}
        set(PKG_CONFIG_EXECUTABLE {{ pkg_config }} CACHE FILEPATH "pkg-config executable")
        {% endif %}
        {% if pkg_config_path %}
        if (DEFINED ENV{PKG_CONFIG_PATH})
        set(ENV{PKG_CONFIG_PATH} "{{ pkg_config_path }}$ENV{PKG_CONFIG_PATH}")
        else()
        set(ENV{PKG_CONFIG_PATH} "{{ pkg_config_path }}")
        endif()
        {% endif %}
        """)

    def context(self):
        pass


class UserToolchain(Block):
    template = textwrap.dedent("""\
        # Include one or more CMake user toolchain from tools.cmake.cmaketoolchain:user_toolchain

        {% for user_toolchain in paths %}
        message(STATUS "Conan toolchain: Including user_toolchain: {{user_toolchain}}")
        include("{{user_toolchain}}")
        {% endfor %}
        """)

    def context(self):
        # This is global [conf] injection of extra toolchain files
        pass


class ExtraFlagsBlock(Block):
    """This block is adding flags directly from user [conf] section"""

    _template = textwrap.dedent("""\
        # Include extra C++, C and linker flags from configuration tools.build:<type>flags
        # and from CMakeToolchain.extra_<type>_flags

        # Conan conf flags start: {{config}}
        {% if cxxflags %}
        string(APPEND CONAN_CXX_FLAGS{{suffix}} "{% for cxxflag in cxxflags %} {{ cxxflag }}{% endfor %}")
        {% endif %}
        {% if cflags %}
        string(APPEND CONAN_C_FLAGS{{suffix}} "{% for cflag in cflags %} {{ cflag }}{% endfor %}")
        {% endif %}
        {% if sharedlinkflags %}
        string(APPEND CONAN_SHARED_LINKER_FLAGS{{suffix}} "{% for sharedlinkflag in sharedlinkflags %} {{ sharedlinkflag }}{% endfor %}")
        {% endif %}
        {% if exelinkflags %}
        string(APPEND CONAN_EXE_LINKER_FLAGS{{suffix}} "{% for exelinkflag in exelinkflags %} {{ exelinkflag }}{% endfor %}")
        {% endif %}
        {% if rcflags %}
        string(APPEND CONAN_RC_FLAGS{{suffix}} "{% for rcflag in rcflags %} {{ rcflag }}{% endfor %}")
        {% endif %}
        {% if defines %}
        {% if config %}
        {% for define in defines %}
        add_compile_definitions("$<$<CONFIG:{{config}}>:{{ define }}>")
        {% endfor %}
        {% else %}
        add_compile_definitions({% for define in defines %} "{{ define }}"{% endfor %})
        {% endif %}
        {% endif %}
        # Conan conf flags end
    """)

    @property
    def template(self):
        pass

    def context(self):
        # Now, it's time to get all the flags defined by the user
        pass


class CMakeFlagsInitBlock(Block):
    template = textwrap.dedent("""\
        # Define CMAKE_<XXX>_FLAGS from CONAN_<XXX>_FLAGS

        foreach(config IN LISTS CMAKE_CONFIGURATION_TYPES)
            string(TOUPPER ${config} config)
            if(DEFINED CONAN_CXX_FLAGS_${config})
              string(APPEND CMAKE_CXX_FLAGS_${config}_INIT " ${CONAN_CXX_FLAGS_${config}}")
            endif()
            if(DEFINED CONAN_C_FLAGS_${config})
              string(APPEND CMAKE_C_FLAGS_${config}_INIT " ${CONAN_C_FLAGS_${config}}")
            endif()
            if(DEFINED CONAN_SHARED_LINKER_FLAGS_${config})
              string(APPEND CMAKE_SHARED_LINKER_FLAGS_${config}_INIT " ${CONAN_SHARED_LINKER_FLAGS_${config}}")
            endif()
            if(DEFINED CONAN_EXE_LINKER_FLAGS_${config})
              string(APPEND CMAKE_EXE_LINKER_FLAGS_${config}_INIT " ${CONAN_EXE_LINKER_FLAGS_${config}}")
            endif()
            if(DEFINED CONAN_RC_FLAGS_${config})
              string(APPEND CMAKE_RC_FLAGS_${config}_INIT " ${CONAN_RC_FLAGS_${config}}")
            endif()
        endforeach()

        if(DEFINED CONAN_CXX_FLAGS)
          string(APPEND CMAKE_CXX_FLAGS_INIT " ${CONAN_CXX_FLAGS}")
        endif()
        if(DEFINED CONAN_C_FLAGS)
          string(APPEND CMAKE_C_FLAGS_INIT " ${CONAN_C_FLAGS}")
        endif()
        if(DEFINED CONAN_SHARED_LINKER_FLAGS)
          string(APPEND CMAKE_SHARED_LINKER_FLAGS_INIT " ${CONAN_SHARED_LINKER_FLAGS}")
        endif()
        if(DEFINED CONAN_EXE_LINKER_FLAGS)
          string(APPEND CMAKE_EXE_LINKER_FLAGS_INIT " ${CONAN_EXE_LINKER_FLAGS}")
        endif()
        if(DEFINED CONAN_RC_FLAGS)
          string(APPEND CMAKE_RC_FLAGS_INIT " ${CONAN_RC_FLAGS}")
        endif()
        if(DEFINED CONAN_OBJCXX_FLAGS)
          string(APPEND CMAKE_OBJCXX_FLAGS_INIT " ${CONAN_OBJCXX_FLAGS}")
        endif()
        if(DEFINED CONAN_OBJC_FLAGS)
          string(APPEND CMAKE_OBJC_FLAGS_INIT " ${CONAN_OBJC_FLAGS}")
        endif()
        """)


class TryCompileBlock(Block):
    template = textwrap.dedent("""\
        # Blocks after this one will not be added when running CMake try/checks
        {% if config %}
        if(NOT DEFINED CMAKE_TRY_COMPILE_CONFIGURATION)  # to allow user command line override
            set(CMAKE_TRY_COMPILE_CONFIGURATION {{config}})
        endif()
        {% endif %}
        get_property( _CMAKE_IN_TRY_COMPILE GLOBAL PROPERTY IN_TRY_COMPILE )
        if(_CMAKE_IN_TRY_COMPILE)
            message(STATUS "Running toolchain IN_TRY_COMPILE")
            return()
        endif()
        """)

    def context(self):
        # Only for well known CMake configurations, but not for custom ones
        # Revert of https://github.com/conan-io/conan/pull/18559, even if it was correct, there are
        # legacy code using check_function_exists that breaks in CMake with MSVC, see
        # https://github.com/conan-io/conan/issues/18689
        # TODO: Resume this effort when other try_compile things are sorted out
        # bt = self._conanfile.settings.get_safe("build_type")
        # config = bt if bt in ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"] else None
        pass


class CompilersBlock(Block):
    template = textwrap.dedent(r"""
        {% for lang, compiler_path in compilers.items() %}
        set(CMAKE_{{ lang }}_COMPILER "{{ compiler_path|replace('\\', '/') }}")
        {% endfor %}
    """)

    def context(self):
        # Reading configuration from "tools.build:compiler_executables" -> {"C": "/usr/bin/gcc"}
        pass


class GenericSystemBlock(Block):
    template = textwrap.dedent("""\
        # Definition of system, platform and toolset

        {% if cmake_sysroot %}
        set(CMAKE_SYSROOT {{ cmake_sysroot }})
        {% endif %}
        {% if cmake_system_name %}
        # Cross building
        if(NOT DEFINED CMAKE_SYSTEM_NAME) # It might have been defined by a user toolchain
        set(CMAKE_SYSTEM_NAME {{ cmake_system_name }})
        endif()
        {% endif %}
        {% if cmake_system_version %}
        if(NOT DEFINED CMAKE_SYSTEM_VERSION) # It might have been defined by a user toolchain
        set(CMAKE_SYSTEM_VERSION {{ cmake_system_version }})
        endif()
        {% endif %}
        {% if cmake_system_processor %}
        if(NOT DEFINED CMAKE_SYSTEM_PROCESSOR) # It might have been defined by a user toolchain
        set(CMAKE_SYSTEM_PROCESSOR {{ cmake_system_processor }})
        endif()
        {% endif %}

        {% if generator_platform and not winsdk_version %}
        set(CMAKE_GENERATOR_PLATFORM "{{ generator_platform }}" CACHE STRING "" FORCE)
        {% elif winsdk_version %}
        if(POLICY CMP0149)
            cmake_policy(GET CMP0149 _POLICY_WINSDK_VERSION)
        endif()
        if(_POLICY_WINSDK_VERSION STREQUAL "NEW")
            message(STATUS "Conan toolchain: CMAKE_GENERATOR_PLATFORM={{gen_platform_sdk_version}}")
            set(CMAKE_GENERATOR_PLATFORM "{{ gen_platform_sdk_version }}" CACHE STRING "" FORCE)
        else()
            # winsdk_version will be taken from above CMAKE_SYSTEM_VERSION
            message(STATUS "Conan toolchain: CMAKE_GENERATOR_PLATFORM={{generator_platform}}")
            set(CMAKE_GENERATOR_PLATFORM "{{ generator_platform }}" CACHE STRING "" FORCE)
        endif()
        {% endif %}

        {% if toolset %}
        message(STATUS "Conan toolchain: CMAKE_GENERATOR_TOOLSET={{ toolset }}")
        set(CMAKE_GENERATOR_TOOLSET "{{ toolset }}" CACHE STRING "" FORCE)
        {% endif %}
        """)

    @staticmethod
    def get_toolset(generator, conanfile):
        pass

    @staticmethod
    def get_generator_platform(generator, conanfile):
        pass

    def _get_generic_system_name(self):
        pass

    def _is_apple_cross_building(self):

        pass

    @staticmethod
    def _get_darwin_version(os_name, os_version):
        # version mapping from https://en.wikipedia.org/wiki/Darwin_(operating_system)
        # but a more detailed version can be found in https://theapplewiki.com/wiki/Kernel
        pass

    def _get_cross_build(self):
        pass

    def _get_winsdk_version(self, system_version, generator_platform):
        pass

    def context(self):
        pass


class ExtraVariablesBlock(Block):
    template = textwrap.dedent("""\
        # Definition of extra CMake variables from tools.cmake.cmaketoolchain:extra_variables

        {% if extra_variables %}
        {% for key, value in extra_variables.items() %}
        set({{ key }} {{ value }})
        {% endfor %}
        {% endif %}
    """)

    def context(self):
        pass


class OutputDirsBlock(Block):

    @property
    def template(self):
        pass

    def _get_cpp_info_value(self, name):
        # Why not taking cpp.build? because this variables are used by the "cmake install"
        # that correspond to the package folder (even if the root is the build directory)
        pass

    def context(self):
        pass


class VariablesBlock(Block):
    @property
    def template(self):
        pass

    def context(self):
        pass


class PreprocessorBlock(Block):
    @property
    def template(self):
        pass

    def context(self):
        pass


class ToolchainBlocks:
    def __init__(self, conanfile, toolchain, items=None):
        self._blocks = {}
        self._conanfile = conanfile
        self._toolchain = toolchain
        if items:
            for name, block in items:
                self._blocks[name] = block(conanfile, toolchain, name)

    def keys(self):
        pass

    def items(self):
        return self._blocks.items()

    def remove(self, name, *args):
        pass

    def select(self, name, *args):
        """
        keep the blocks provided as arguments, remove the others, except pre-existing "variables"
        and "preprocessor", to not break behavior
        """
        pass

    def enabled(self, name, *args):
        """
        keep the blocks provided as arguments, remove the others
        """
        pass

    def __setitem__(self, name, block_type):
        # Create a new class inheriting Block with the elements of the provided one
        block_type = type('proxyUserBlock', (Block,), dict(block_type.__dict__))
        self._blocks[name] = block_type(self._conanfile, self._toolchain, name)

    def __getitem__(self, name):
        return self._blocks[name]

    def process_blocks(self):
        pass
