import os
import textwrap

from conan.tools.cmake.cmakedeps import FIND_MODE_NONE, FIND_MODE_CONFIG, FIND_MODE_MODULE, \
    FIND_MODE_BOTH
from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate
from conan.errors import ConanException
from conan.internal.api.install.generators import relativize_path
from conan.tools.cmake.utils import cmake_escape_value

"""

foo-release-x86_64-data.cmake

"""


class ConfigDataTemplate(CMakeDepsFileTemplate):

    @property
    def filename(self):
        pass

    @property
    def _build_modules_activated(self):
        pass

    @property
    def context(self):
        pass

    @property
    def cmake_package_type(self):
        pass

    @property
    def is_host_windows(self):
        # to account for all WindowsStore, WindowsCE and Windows OS in settings
        pass

    @property
    def template(self):
        # This will be at: XXX-release-data.cmake
        pass

    def _get_global_cpp_cmake(self):
        pass

    @property
    def _root_folder(self):
        pass

    def _get_required_components_cpp(self):
        """Returns a list of (component_name, DepsCppCMake)"""
        pass

    def _get_dependency_filenames(self):
        pass

    def _get_dependencies_find_modes(self):
        pass


class _TargetDataContext:

    def __init__(self, cpp_info, pfolder_var_name, package_folder, require, library_type,
                 is_host_windows, conanfile, cmakedeps, comp_name=None):

        def join_paths(paths):
            """
            Paths are doubled quoted, and escaped (but spaces)
            e.g: set(LIBFOO_INCLUDE_DIRS "/path/to/included/dir" "/path/to/included/dir2")
            """
            pass

        def join_flags(separator, values):
            # Flags have to be escaped
            pass

        def join_defines(values, prefix=""):
            # Defines have to be escaped, included spaces
            pass

        self.include_paths = join_paths(cpp_info.includedirs)
        self.lib_paths = join_paths(cpp_info.libdirs)
        self.res_paths = join_paths(cpp_info.resdirs)
        self.bin_paths = join_paths(cpp_info.bindirs)
        self.build_paths = join_paths(cpp_info.builddirs)
        self.framework_paths = join_paths(cpp_info.frameworkdirs)
        self.libs = join_flags(" ", cpp_info.libs)
        self.system_libs = join_flags(" ", cpp_info.system_libs)
        self.frameworks = join_flags(" ", cpp_info.frameworks)
        self.defines = join_defines(cpp_info.defines, "-D")
        self.compile_definitions = join_defines(cpp_info.defines)
        self.library_type = library_type
        self.is_host_windows = "1" if is_host_windows else "0"

        # For modern CMake targets we need to prepare a list to not
        # loose the elements in the list by replacing " " with ";". Example "-framework Foundation"
        # Issue: #1251
        self.cxxflags_list = join_flags(";", cpp_info.cxxflags)
        self.cflags_list = join_flags(";", cpp_info.cflags)

        # linker flags without magic: trying to mess with - and / =>
        # https://github.com/conan-io/conan/issues/8811
        # frameworks should be declared with cppinfo.frameworks not "-framework Foundation"
        self.sharedlinkflags_list = '"{}"'.format(join_flags(";", cpp_info.sharedlinkflags)) \
            if cpp_info.sharedlinkflags else ''
        self.exelinkflags_list = '"{}"'.format(join_flags(";", cpp_info.exelinkflags)) \
            if cpp_info.exelinkflags else ''

        self.objects_list = join_paths(cpp_info.objects)

        # traits logic
        if require and not require.headers:
            self.include_paths = ""
        if require and not require.libs:
            # self.lib_paths = ""  IMPORTANT! LINKERS IN LINUX FOR SHARED MIGHT NEED IT EVEN IF
            #                      NOT REALLY LINKING LIB
            self.libs = ""
            if cpp_info.frameworkdirs:  # Only invalidate for in-package frameworks
                # FIXME: The mix of in-package frameworks + system ones is broken
                self.frameworks = ""
        if require and not require.libs and not require.headers:
            self.defines = ""
            self.compile_definitions = ""
            self.cxxflags_list = ""
            self.cflags_list = ""
            self.sharedlinkflags_list = ""
            self.exelinkflags_list = ""
            self.objects_list = ""
        if require and not require.run:
            self.bin_paths = ""

        build_modules = cmakedeps.get_property("cmake_build_modules", conanfile, check_type=list) or []
        self.build_modules_paths = join_paths(build_modules)
        # SONAME flag only makes sense for SHARED libraries
        nosoname = cmakedeps.get_property("nosoname", conanfile, comp_name, check_type=bool)
        self.no_soname = str((nosoname if self.library_type == "SHARED" else False) or False).upper()
