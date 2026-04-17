"""
    This is a helper class which offers a lot of useful methods and attributes
"""
# FIXME: only for tools.gnu? perhaps it should be a global module

from conan.tools.apple.apple import is_apple_os
from conan.tools.microsoft import is_msvc
from conan.internal.subsystems import subsystem_path, deduce_subsystem


class GnuDepsFlags:

    def __init__(self, conanfile, cpp_info):
        self._conanfile = conanfile
        self._subsystem = deduce_subsystem(conanfile, scope="build")

        # From cppinfo, calculated flags
        self.include_paths = self._format_include_paths(cpp_info.includedirs)
        self.lib_paths = self._format_library_paths(cpp_info.libdirs)
        self.defines = self._format_defines(cpp_info.defines)
        self.libs = self._format_libraries(cpp_info.libs)
        self.frameworks = self._format_frameworks(cpp_info.frameworks)
        self.framework_paths = self._format_frameworks(cpp_info.frameworkdirs, is_path=True)

        # Direct flags
        self.cxxflags = cpp_info.cxxflags or []
        self.cflags = cpp_info.cflags or []
        self.sharedlinkflags = cpp_info.sharedlinkflags or []
        self.exelinkflags = cpp_info.exelinkflags or []
        self.system_libs = self._format_libraries(cpp_info.system_libs)

        # Not used?
        # self.bin_paths
        # self.build_paths
        # self.src_paths

    _GCC_LIKE = ['clang', 'apple-clang', 'gcc']

    @staticmethod
    def _format_defines(defines):
        pass

    def _format_frameworks(self, frameworks, is_path=False):
        """
        returns an appropriate compiler flags to link with Apple Frameworks
        or an empty array, if Apple Frameworks aren't supported by the given compiler
        """
        pass

    def _format_include_paths(self, include_paths):
        pass

    def _format_library_paths(self, library_paths):
        pass

    def _format_libraries(self, libraries):
        pass

    def _adjust_path(self, path):
        pass
