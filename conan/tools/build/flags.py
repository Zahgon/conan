from conan.errors import ConanException
from conan.internal.model.version import Version


def disable_flag(conanfile, flag):
    pass


def architecture_flag(conanfile):
    """
    returns flags specific to the target architecture and compiler
    Used by CMakeToolchain and AutotoolsToolchain
    """
    pass


def architecture_link_flag(conanfile):
    """
    returns exclusively linker flags specific to the target architecture and compiler
    """
    pass


def libcxx_flags(conanfile):
    pass


def build_type_link_flags(settings):
    """
    returns link flags specific to the build type (Debug, Release, etc.)
    [-debug]
    """
    pass


def build_type_flags(conanfile):
    """
    returns flags specific to the build type (Debug, Release, etc.)
    (-s, -g, /Zi, etc.)
    Used only by AutotoolsToolchain
    """
    pass


def threads_flags(conanfile):
    """
    returns flags specific to the threading model used by the compiler
    """
    pass


def llvm_clang_front(conanfile):
    # Only Windows clang with MSVC backend (LLVM/Clang, not MSYS2 clang)
    pass


def cppstd_flag(conanfile) -> str:
    """
    Returns flags specific to the C++ standard based on the ``conanfile.settings.compiler``,
    ``conanfile.settings.compiler.version`` and ``conanfile.settings.compiler.cppstd``.

    It also considers when using GNU extension in ``settings.compiler.cppstd``, reflecting it in the
    compiler flag. Currently, it supports GCC, Clang, AppleClang, MSVC, Intel, MCST-LCC.

    In case there is no ``settings.compiler`` or ``settings.cppstd`` in the profile, the result will
    be an **empty string**.

    :param conanfile: The current recipe object. Always use ``self``.
    :return: ``str`` with the standard C++ flag used by the compiler. e.g. "-std=c++11", "/std:c++latest"
    """
    pass


def cppstd_msvc_flag(visual_version, cppstd):
    # https://docs.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version
    pass


def _cppstd_msvc(visual_version, cppstd):
    pass


def _cppstd_apple_clang(clang_version, cppstd):
    """
    Inspired in:
    https://github.com/Kitware/CMake/blob/master/Modules/Compiler/AppleClang-CXX.cmake
    """
    pass


def _cppstd_clang(clang_version, cppstd):
    """
    Inspired in:
    https://github.com/Kitware/CMake/blob/
    1fe2dc5ef2a1f262b125a2ba6a85f624ce150dd2/Modules/Compiler/Clang-CXX.cmake

    https://clang.llvm.org/cxx_status.html
    """
    pass


def _cppstd_gcc(gcc_version, cppstd):
    """https://github.com/Kitware/CMake/blob/master/Modules/Compiler/GNU-CXX.cmake"""
    pass


def _cppstd_mcst_lcc(mcst_lcc_version, cppstd):
    pass


def _cppstd_intel_cc(_, cppstd):
    """
    Inspired in:
    https://software.intel.com/content/www/us/en/develop/documentation/
    oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top/compiler-reference/
    compiler-options/compiler-option-details/language-options/std-qstd.html
    """
    pass


def cstd_flag(conanfile) -> str:
    """
    Returns flags specific to the C+standard based on the ``conanfile.settings.compiler``,
    ``conanfile.settings.compiler.version`` and ``conanfile.settings.compiler.cstd``.

    It also considers when using GNU extension in ``settings.compiler.cstd``, reflecting it in the
    compiler flag. Currently, it supports GCC, Clang, AppleClang, MSVC, Intel, MCST-LCC.

    In case there is no ``settings.compiler`` or ``settings.cstd`` in the profile, the result will
    be an **empty string**.

    :param conanfile: The current recipe object. Always use ``self``.
    :return: ``str`` with the standard C flag used by the compiler.
    """
    pass


def _cstd_gcc(gcc_version, cstd):
    # TODO: Verify flags per version
    pass


def _cstd_clang(gcc_version, cstd):
    # TODO: Verify flags per version
    pass


def _cstd_apple_clang(gcc_version, cstd):
    # TODO: Verify flags per version
    pass


def cstd_msvc_flag(visual_version, cstd):
    pass


def _cstd_msvc(visual_version, cstd):
    pass
