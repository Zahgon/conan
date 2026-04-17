import copy
import hashlib
import numbers
import platform
import re
import os
import fnmatch
import textwrap

from jinja2 import Environment, FileSystemLoader

from conan.errors import ConanException
from conan.internal.api.detect import detect_api
from conan.internal.cache.home_paths import HomePaths
from conan.internal.model.options import _PackageOption
from conan.internal.model.recipe_ref import ref_matches
from conan.internal.model.settings import SettingsItem
from conan.internal.util.files import load, save

BUILT_IN_CONFS = {
    "core:required_conan_version": "Raise if current version does not match the defined range.",
    "core:non_interactive": "Disable interactive user input, raises error if input necessary",
    "core:warnings_as_errors": "Treat warnings matching any of the patterns in this list as errors and then raise an exception. "
                               "Current warning tags are 'network', 'deprecated'",
    "core:skip_warnings": "Do not show warnings matching any of the patterns in this list. "
                          "Current warning tags are 'network', 'deprecated', 'experimental'",
    "core:default_profile": "Defines the default host profile ('default' by default)",
    "core:default_build_profile": "Defines the default build profile ('default' by default)",
    "core:allow_uppercase_pkg_names": "Temporarily (will be removed in 2.X) allow uppercase names",
    "core.version_ranges:resolve_prereleases": "Whether version ranges can resolve to pre-releases or not",
    "core.upload:retry": "(int, default: 1) Number of retries in case of failure when uploading to Conan server",
    "core.upload:retry_wait": "(int, default: 5s) Seconds to wait between upload attempts to Conan server",
    "core.upload:parallel": "Number of concurrent threads to upload packages",
    "core.download:parallel": "Number of concurrent threads to download packages",
    "core.download:retry": " (int, default: 2) Number of retries in case of failure when downloading from Conan server",
    "core.download:retry_wait": "(int, default: 1s) Seconds to wait between download attempts from Conan server",
    "core.download:download_cache": "Define path to a file download cache",
    "core.cache:storage_path": "Absolute path where the packages and database are stored",
    "core:update_policy": "(Legacy). If equal 'legacy' when multiple remotes, update based on order of remotes, only the timestamp of the first occurrence of each revision counts.",
    # Sources backup
    "core.sources:download_cache": "Folder to store the sources backup",
    "core.sources:download_urls": "List of URLs to download backup sources from",
    "core.sources:upload_url": "Remote URL to upload backup sources to",
    "core.sources:exclude_urls": "URLs which will not be backed up",
    "core.sources.patch:extra_path": "Extra path to search for patch files for conan create",
    # Package ID
    "core.package_id:default_unknown_mode": "By default, 'semver_mode'",
    "core.package_id:default_non_embed_mode": "By default, 'minor_mode'",
    "core.package_id:default_embed_mode": "By default, 'full_mode'",
    "core.package_id:default_python_mode": "By default, 'minor_mode'",
    "core.package_id:default_build_mode": "By default, 'None'",
    "core.package_id:config_mode": "How the 'config_version' affects binaries. By default 'None'",
    # General HTTP(python-requests) configuration
    "core.net.http:max_retries": "Maximum number of connection retries (requests library)",
    "core.net.http:timeout": "Number of seconds without response to timeout (requests library)",
    "core.net.http:no_proxy_match": "List of urls to skip from proxies configuration",
    "core.net.http:proxies": "Dictionary containing the proxy configuration",
    "core.net.http:cacert_path": "Path containing a custom Cacert file",
    "core.net.http:client_cert": "Path or tuple of files containing a client cert (and key)",
    "core.net.http:clean_system_proxy": "If defined, the proxies system env-vars will be discarded",
    # Compression for `conan upload`
    "core.upload:compression_format": "The compression format used when uploading Conan packages. "
                                      "Possible values: 'zst', 'xz', 'gz' (default=gz)",
    "core.gzip:compresslevel": "The Gzip compression level for Conan artifacts (default=9)",
    "core:compresslevel": "The compression level for Conan artifacts (default zstd=3, gz=9)",
    # Excluded from revision_mode = "scm" dirty and Git().is_dirty() checks
    "core.scm:excluded": "List of excluded patterns for builtin git dirty checks",
    "core.scm:local_url": "By default allows to store local folders as remote url, but not upload them. Use 'allow' for allowing upload and 'block' to completely forbid it",
    # Compatibility opt-in, to be removed in future versions as optimized behavior becomes default
    "core.graph:compatibility_mode": "(Experimental) Set this to 'optimized' to enable the improved compatibility behaviour when querying multiple compatible binaries in remotes",
    # Tools
    "tools.android:ndk_path": "Argument for the CMAKE_ANDROID_NDK",
    "tools.android:cmake_legacy_toolchain": "Define to explicitly pass ANDROID_USE_LEGACY_TOOLCHAIN_FILE in CMake toolchain",
    "tools.build:skip_test": "Do not execute CMake.test() and Meson.test() when enabled",
    "tools.build:download_source": "Force download of sources for every package",
    "tools.build:jobs": "Default compile jobs number -jX Ninja, Make, /MP VS (default: max CPUs)",
    "tools.build:sysroot": "Pass the --sysroot=<tools.build:sysroot> flag if available. (None by default)",
    "tools.build:add_rpath_link": "Add -Wl,-rpath-link flags pointing to all lib directories for host dependencies (CMake and Meson toolchains)",
    "tools.build.cross_building:can_run": "(boolean) Indicates whether is possible to run a non-native app on the same architecture. It's used by 'can_run' tool",
    "tools.build.cross_building:cross_build": "(boolean) Decides whether cross-building or not regardless of arch/OS settings. Used by 'cross_building' tool",
    "tools.build:verbosity": "Verbosity of build systems if set. Possible values are 'quiet' and 'verbose'",
    "tools.compilation:verbosity": "Verbosity of compilation tools if set. Possible values are 'quiet' and 'verbose'",
    "tools.cmake.cmaketoolchain:generator": "User defined CMake generator to use instead of default",
    "tools.cmake.cmaketoolchain:find_package_prefer_config": "Argument for the CMAKE_FIND_PACKAGE_PREFER_CONFIG",
    "tools.cmake.cmaketoolchain:toolchain_file": "Use other existing file rather than conan_toolchain.cmake one",
    "tools.cmake.cmaketoolchain:user_toolchain": "Inject existing user toolchains at the beginning of conan_toolchain.cmake",
    "tools.cmake.cmaketoolchain:system_name": "Define CMAKE_SYSTEM_NAME in CMakeToolchain",
    "tools.cmake.cmaketoolchain:system_version": "Define CMAKE_SYSTEM_VERSION in CMakeToolchain",
    "tools.cmake.cmaketoolchain:system_processor": "Define CMAKE_SYSTEM_PROCESSOR in CMakeToolchain",
    "tools.cmake.cmaketoolchain:toolset_arch": "Toolset architecture to be used as part of CMAKE_GENERATOR_TOOLSET in CMakeToolchain",
    "tools.cmake.cmaketoolchain:toolset_cuda": "(Experimental) Path to a CUDA toolset to use, or version if installed at the system level",
    "tools.cmake.cmaketoolchain:presets_environment": "String to define wether to add or not the environment section to the CMake presets. Empty by default, will generate the environment section in CMakePresets. Can take values: 'disabled'.",
    "tools.cmake.cmaketoolchain:extra_variables": "Dictionary with variables to be injected in CMakeToolchain (potential override of CMakeToolchain defined variables)",
    "tools.cmake.cmaketoolchain:enabled_blocks": "Select the specific blocks to use in the conan_toolchain.cmake",
    "tools.cmake.cmaketoolchain:user_presets": "(Experimental) Select a different name instead of CMakeUserPresets.json, empty to disable",
    "tools.cmake.cmake_layout:build_folder_vars": "Settings and Options that will produce a different build folder and different CMake presets names",
    "tools.cmake.cmake_layout:build_folder": "(Experimental) Allow configuring the base folder of the build for local builds",
    "tools.cmake.cmake_layout:test_folder": "(Experimental) Allow configuring the base folder of the build for test_package",
    "tools.cmake:cmake_program": "Path to CMake executable",
    "tools.cmake.cmakedeps:new": "Use the new CMakeDeps generator",
    "tools.cmake:ctest_args": "Add extra arguments to CMake.ctest() runner command line",
    "tools.cmake:configure_args": "Add extra arguments to CMake.configure() command line ",
    "tools.cmake:install_strip": "(Deprecated) Add --strip to cmake.install(). Use tools.build:install_strip instead",
    "tools.deployer:symlinks": "Set to False to disable deployers copying symlinks",
    "tools.files.download:retry": "(int, default: 2) Number of retries in case of failure when downloading",
    "tools.files.download:retry_wait": "(int, default: 5s) Seconds to wait between download attempts",
    "tools.files.download:verify": "If set, overrides recipes on whether to perform SSL verification for their downloaded files. Only recommended to be set while testing",
    "tools.files.unzip:filter": "Define tar extraction filter: 'fully_trusted', 'tar', 'data'",
    "tools.graph:vendor": "(Experimental) If 'build', enables the computation of dependencies of vendoring packages to build them",
    "tools.graph:skip_binaries": "Allow the graph to skip binaries not needed in the current configuration (True by default)",
    "tools.graph:skip_build": "(Experimental) Do not expand build/tool_requires",
    "tools.graph:skip_test": "(Experimental) Do not expand test_requires. If building it might need 'tools.build:skip_test=True'",
    "tools.gnu:make_program": "Indicate path to make program",
    "tools.gnu:disable_flags": "Disable the automatic addition of flags to some build systems. List of possible values: ['arch', 'arch_link', 'libcxx', 'build_type', 'build_type_link', 'threads','cppstd', 'cstd']",
    "tools.gnu:define_libcxx11_abi": "Force definition of GLIBCXX_USE_CXX11_ABI=1 for libstdc++11",
    "tools.gnu:pkg_config": "Path to pkg-config executable used by PkgConfig build helper",
    "tools.gnu:build_triplet": "Custom build triplet to pass to Autotools scripts",
    "tools.gnu:host_triplet": "Custom host triplet to pass to Autotools scripts",
    "tools.gnu:extra_configure_args": "List of extra arguments to pass to configure when using AutotoolsToolchain and GnuToolchain",
    "tools.google.bazel:configs": "List of Bazel configurations to be used as 'bazel build --config=config1 ...'",
    "tools.google.bazel:bazelrc_path": "List of paths to bazelrc files to be used as 'bazel --bazelrc=rcpath1 ... build'",
    "tools.meson.mesontoolchain:backend": "Any Meson backend: ninja, vs, vs2010, vs2012, vs2013, vs2015, vs2017, vs2019, xcode",
    "tools.meson.mesontoolchain:extra_machine_files": "List of paths for any additional native/cross file references to be appended to the existing Conan ones",
    "tools.microsoft:winsdk_version": "Use this winsdk_version in vcvars",
    "tools.microsoft:msvc_update": "Force the specific update irrespective of compiler.update (CMakeToolchain and VCVars)",
    "tools.microsoft.msbuild:vs_version": "Defines the IDE version (15, 16, 17) when using the msvc compiler. Necessary if compiler.version specifies a toolset that is not the IDE default",
    "tools.microsoft.msbuild:max_cpu_count": "Argument for the /m when running msvc to build parallel projects",
    "tools.microsoft.msbuild:installation_path": "VS install path, to avoid auto-detect via vswhere, like C:/Program Files (x86)/Microsoft Visual Studio/2019/Community. Use empty string to disable",
    "tools.microsoft.msbuilddeps:exclude_code_analysis": "Suppress MSBuild code analysis for patterns",
    "tools.microsoft.msbuildtoolchain:compile_options": "Dictionary with MSBuild compiler options",
    "tools.microsoft.bash:subsystem": "The subsystem to be used when conanfile.win_bash==True. Possible values: msys2, msys, cygwin, wsl, sfu",
    "tools.microsoft.bash:path": "The path to the shell to run when conanfile.win_bash==True",
    "tools.microsoft.bash:active": "Set True only when Conan runs in a POSIX Bash (MSYS2/Cygwin) where Python's subprocess (shell=True) uses a POSIX-compatible shell (e.g., /bin/sh). Do not set when using Conan from cmd/PowerShell or with native Windows Python ('win32').",
    "tools.intel:installation_path": "Defines the Intel oneAPI installation root path",
    "tools.intel:setvars_args": "Custom arguments to be passed onto the setvars.sh|bat script from Intel oneAPI",
    "tools.system.package_manager:tool": "Default package manager tool: 'apk', 'apt-get', 'yum', 'dnf', 'brew', 'pacman', 'choco', 'zypper', 'pkg' or 'pkgutil'",
    "tools.system.package_manager:mode": "Mode for package_manager tools: 'check', 'report', 'report-installed' or 'install'",
    "tools.system.package_manager:sudo": "Use 'sudo' when invoking the package manager tools in Linux (False by default)",
    "tools.system.package_manager:sudo_askpass": "Use the '-A' argument if using sudo in Linux to invoke the system package manager (False by default)",
    "tools.system.pyenv:python_interpreter": "(Experimental) Path to the Python interpreter to be used to create the virtualenv",
    "tools.system.pipenv:python_interpreter": "(Deprecated) Use 'tools.system.pyenv:python_interpreter' instead. Path to the Python interpreter to be used to create the virtualenv",
    "tools.apple:sdk_path": "Path to the SDK to be used",
    "tools.apple:enable_bitcode": "(boolean) Enable/Disable Bitcode Apple Clang flags",
    "tools.apple:enable_arc": "(boolean) Enable/Disable ARC Apple Clang flags",
    "tools.apple:enable_visibility": "(boolean) Enable/Disable Visibility Apple Clang flags",
    "tools.env.virtualenv:powershell": "If specified, it generates PowerShell launchers (.ps1). Use this configuration setting the PowerShell executable you want to use (e.g., 'powershell.exe' or 'pwsh'). Setting it to True or False is deprecated as of Conan 2.11.0.",
    "tools.env:dotenv": "(Experimental) Generate dotenv environment files",
    "tools.env:deactivation_mode": "(Experimental) If 'function', generate a deactivate function instead of a script to unset the environment variables",
    # Compilers/Flags configurations
    "tools.build:compiler_executables": "Defines a Python dict-like with the compilers path to be used. Allowed keys {'c', 'cpp', 'cuda', 'objc', 'objcxx', 'rc', 'fortran', 'asm', 'hip', 'ispc'}",
    "tools.build:cxxflags": "List of extra CXX flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain",
    "tools.build:cflags": "List of extra C flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain",
    "tools.build:defines": "List of extra definition flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain",
    "tools.build:sharedlinkflags": "List of extra flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain",
    "tools.build:exelinkflags": "List of extra flags used by different toolchains like CMakeToolchain, AutotoolsToolchain and MesonToolchain",
    "tools.build:rcflags": "List of extra RC (resource compiler) flags used by different toolchains like CMakeToolchain, MSBuildToolchain and MesonToolchain",
    "tools.build:linker_scripts": "List of linker script files to pass to the linker used by different toolchains like CMakeToolchain, AutotoolsToolchain, and MesonToolchain",
    # Toolchain installation
    "tools.build:install_strip": "(boolean or list) True/False to strip on install for every CMake, Meson and Autotools "
                                 "integration, or a list of 'cmake', 'meson', 'autotools' to strip only for those.",
    # Package ID composition
    "tools.info.package_id:confs": "List of existing configuration to be part of the package ID",
}

BUILT_IN_CONFS = {key: value for key, value in sorted(BUILT_IN_CONFS.items())}


_BUILT_IN_CONFS_TYPES = {
    "core:required_conan_version": str,
    "tools.microsoft:msvc_update": str
}

CORE_CONF_PATTERN = re.compile(r"^(core\..+|core):.*")
TOOLS_CONF_PATTERN = re.compile(r"^(tools\..+|tools):.*")
USER_CONF_PATTERN = re.compile(r"^(user\..+|user):.*")


def _is_profile_module(module_name):
    # These are the modules that are propagated to profiles and user recipes
    pass


# FIXME: Refactor all the next classes because they are mostly the same as
#        conan.tools.env.environment ones
class _ConfVarPlaceHolder:
    pass


class _ConfValue:

    def __init__(self, name, value, path=False, update=None, important=False):
        self.name = name
        self._important = important
        self._value = value
        self._value_type = type(value)
        self._path = path
        self._update = update

    @staticmethod
    def parse(name, value, path=False, update=None):
        pass

    def __repr__(self):
        return repr(self._value)

    @property
    def value(self):
        pass

    def copy(self):
        # Using copy for when self._value is a mutable list
        pass

    def dumps(self):
        pass

    def serialize(self):
        pass

    def update(self, value):
        assert self._value_type is dict, "Only dicts can be updated"
        assert isinstance(value, dict), "Only dicts can update"
        self._value.update(value)

    def remove(self, value):
        pass

    def append(self, value):
        pass

    def prepend(self, value):
        pass

    def compose_conf_value(self, other):
        """
        self has precedence, the "other" will add/append if possible and not conflicting, but
        self mandates what to do. If self has define(), without placeholder, that will remain.
        :type other: _ConfValue
        """
        pass

    def set_relative_base_folder(self, folder):
        pass


class Conf:
    # Putting some default expressions to check that any value could be false
    boolean_false_expressions = ("0", '"0"', "false", '"false"', "off")
    boolean_true_expressions = ("1", '"1"', "true", '"true"', "on")

    def __init__(self):
        # It being ordered allows for Windows case-insensitive composition
        self._values = {}  # {var_name: [] of values, including separators}

    def __bool__(self):
        return bool(self._values)

    def clear(self):
        pass

    def validate(self):
        pass

    def items(self):
        # FIXME: Keeping backward compatibility
        for k, v in self._values.items():
            yield k, v.value

    def get(self, conf_name, default=None, check_type=None, choices=None):
        """
        Get all the values of the given configuration name.

        :param conf_name: Name of the configuration.
        :param default: Default value in case of conf does not have the conf_name key.
        :param check_type: Check the conf type(value) is the same as the given by this param.
                           There are two default smart conversions for bool and str types.
        :param choices: list of possible values this conf can have, if value not in it, errors.
        """
        # Skipping this check only the user.* configurations
        self._check_conf_name(conf_name)

        conf_value = self._values.get(conf_name)
        if conf_value:
            v = conf_value.value
            if v is None:  # value was unset
                return default
            if choices is not None and v not in choices:
                raise ConanException(f"Unknown value '{v}' for '{conf_name}'")
            # Some smart conversions
            if check_type is bool and not isinstance(v, bool):
                if str(v).lower() in Conf.boolean_false_expressions:
                    return False
                if str(v).lower() in Conf.boolean_true_expressions:
                    return True
                raise ConanException(f"[conf] {conf_name} must be a boolean-like object "
                                     f"(true/false, 1/0, on/off) and value '{v}' does not match it.")
            elif check_type is str and not isinstance(v, str):
                # TODO: this would be converting things like lists to strings without
                #   proper error, is it worth trying to change it?
                return str(v)
            elif (check_type is not None and not isinstance(v, check_type) or
                  check_type is int and isinstance(v, bool)):
                raise ConanException(f"[conf] {conf_name} must be a "
                                     f"{check_type.__name__}-like object. The value '{v}' "
                                     f"introduced is a {type(v).__name__} object")
            return v
        else:
            return default

    def pop(self, conf_name, default=None):
        """
        Remove the given configuration, returning its value.

        :param conf_name: Name of the configuration.
        :param default: Default value to return in case the configuration doesn't exist.
        :return:
        """
        value = self.get(conf_name, default=default)
        self._values.pop(conf_name, None)
        return value

    def show(self, fnpattern, pattern=""):
        pass

    def copy(self):
        pass

    def filter_core(self):
        pass

    def dumps(self):
        """
        Returns a string with the format ``name=conf-value``
        """
        pass

    def serialize(self):
        """
        Returns a dict-like object, e.g., ``{"tools.xxxx": "value1"}``
        """
        pass

    def define(self, name, value):
        """
        Define a value for the given configuration name.

        :param name: Name of the configuration.
        :param value: Value of the configuration.
        """
        pass

    def define_path(self, name, value):
        pass

    def unset(self, name):
        """
        Clears the variable, equivalent to a unset or set XXX=

        :param name: Name of the configuration.
        """
        pass

    def update(self, name, value):
        """
        Update the value to the given configuration name.

        :param name: Name of the configuration.
        :param value: Value of the configuration.
        """
        # Placeholder trick is not good for dict update, so we need to explicitly update=True
        conf_value = _ConfValue.parse(name, {}, update=True)
        self._values.setdefault(conf_value.name, conf_value).update(value)

    def update_path(self, name, value):
        pass

    def append(self, name, value):
        """
        Append a value to the given configuration name.

        :param name: Name of the configuration.
        :param value: Value to append.
        """
        pass

    def append_path(self, name, value):
        pass

    def prepend(self, name, value):
        """
        Prepend a value to the given configuration name.

        :param name: Name of the configuration.
        :param value: Value to prepend.
        """
        pass

    def prepend_path(self, name, value):
        pass

    def remove(self, name, value):
        """
        Remove a value from the given configuration name.

        :param name: Name of the configuration.
        :param value: Value to remove.
        """
        pass

    def compose_conf(self, other):
        """
        :param other: other has less priority than current one
        :type other: Conf
        """
        pass

    def copy_conaninfo_conf(self):
        """
        Get a new `Conf()` object with all the configurations required by the consumer
        to be included in the final `ConanInfo().package_id()` computation. For instance, let's
        suppose that we have this Conan `profile`:

        ```
        pass
        [conf]
        tools.info.package_id:confs=["tools.build:cxxflags", "tools.build:cflags"]
        tools.build:cxxflags=["flag1xx"]
        tools.build:cflags=["flag1"]
        tools.build:defines=["DEF1"]
        pass

        Then, the resulting `Conf()` will have only these configuration lines:

        tools.build:cxxflags=["flag1xx"]
        tools.build:cflags=["flag1"]
        ```

        :return: a new `< Conf object >` with the configuration selected by `tools.info.package_id:confs`.
        """
        pass

    def set_relative_base_folder(self, folder):
        pass

    @staticmethod
    def _check_conf_name(conf):
        pass


class ConfDefinition:
    # Order is important, "define" must be latest
    actions = (("+=", "append"), ("=+", "prepend"),
               ("=!", "unset"), ("*=", "update"), ("=", "define"))

    def __init__(self):
        self._pattern_confs = {}

    def __bool__(self):
        return bool(self._pattern_confs)

    def get(self, conf_name, default=None, check_type=None, choices=None):
        """
        Get the value of the conf name requested and convert it to the [type]-like passed.
        """
        pattern, name = self._split_pattern_name(conf_name)
        return self._pattern_confs.get(pattern, Conf()).get(name, default=default,
                                                            check_type=check_type, choices=choices)

    def show(self, fnpattern):
        """
        Get the value of the confs that match the requested pattern
        """
        pass

    def pop(self, conf_name, default=None):
        """
        Remove the conf name passed.
        """
        pattern, name = self._split_pattern_name(conf_name)
        return self._pattern_confs.get(pattern, Conf()).pop(name, default=default)

    @staticmethod
    def _split_pattern_name(pattern_name):
        pass

    def get_conanfile_conf(self, ref, is_consumer=False):
        """ computes package-specific Conf
        it is only called when conanfile.buildenv is called
        the last one found in the profile file has top priority
        """
        pass

    def update_conf_definition(self, other):
        """
        :type other: ConfDefinition
        :param other: The argument profile has priority/precedence over the current one.
        """
        pass

    def _update_conf_definition(self, pattern, conf):
        pass

    def rebase_conf_definition(self, global_conf):
        """
        for taking the new global.conf and composing with the profile [conf]
        :type global_conf: ConfDefinition
        """
        pass

    def update(self, key, value, profile=False, method="define"):
        """
        Define/append/prepend/unset any Conf line
        >> update("tools.build:verbosity", "verbose")
        """
        pattern, name = self._split_pattern_name(key)

        if not _is_profile_module(name):
            if profile:
                raise ConanException("[conf] '{}' not allowed in profiles".format(key))
            if pattern is not None:
                raise ConanException("Conf '{}' cannot have a package pattern".format(key))

        # strip whitespaces before/after =
        # values are not strip() unless they are a path, to preserve potential whitespaces
        name = name.strip()

        # When loading from profile file, latest line has priority
        conf = Conf()
        if method == "unset":
            conf.unset(name)
        else:
            getattr(conf, method)(name, value)
        # Update
        self._update_conf_definition(pattern, conf)

    def dumps(self):
        pass

    def serialize(self):
        pass

    @staticmethod
    def _get_evaluated_value(_v):
        """
        Function to avoid eval() catching local variables
        """
        pass

    def loads(self, text, profile=False):
        pass

    def validate(self):
        pass

    def clear(self):
        pass


def load_global_conf(home_folder):
    pass
