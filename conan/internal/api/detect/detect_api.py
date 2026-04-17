import os
import platform
import re
import tempfile
import textwrap

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.model.version import Version
from conan.internal.util.files import load, save
from conan.internal.util.runners import check_output_runner, detect_runner


def detect_os():
    pass


def detect_arch():
    pass


def _get_solaris_architecture():
    # under intel solaris, platform.machine()=='i86pc' so we need to handle
    # it early to suport 64-bit
    pass


def _get_aix_conf(options=None):
    pass


def _get_aix_architecture():
    pass


def _get_e2k_architecture():
    pass


def _parse_gnu_libc(ldd_output):
    pass


def _detect_gnu_libc(ldd="/usr/bin/ldd"):
    pass


def _parse_musl_libc(ldd_output):
    pass


def _detect_musl_libc(ldd="/usr/bin/ldd"):
    pass


def detect_libc(ldd="/usr/bin/ldd"):
    pass


def detect_libcxx(compiler, version, compiler_exe=None):
    pass


def default_msvc_runtime(compiler):
    pass


def detect_msvc_update(version):
    pass


def default_cppstd(compiler, compiler_version):
    """ returns the default cppstd for the compiler-version. This is not detected, just the default
    """
    pass


def detect_cppstd(compiler, compiler_version):
    pass


def default_cstd(compiler, compiler_version):
    """returns the default cstd for the compiler-version. This is not detected, just the default"""
    pass


def detect_default_compiler():
    """
        find the default compiler on the build machine
        search order and priority:
        1. CC and CXX environment variables are always top priority
        2. Visual Studio detection (Windows only) via vswhere or registry or environment variables
        3. Apple Clang (Mac only)
        4. cc executable
        5. gcc executable
        6. clang executable
        """
    pass


def default_msvc_ide_version(version):
    pass


def _detect_vs_ide_version():
    pass


def _cc_compiler(compiler_exe="cc"):
    # Try to detect the "cc" linux system "alternative". It could point to gcc or clang
    pass


def detect_gcc_compiler(compiler_exe="gcc"):
    pass


def detect_compiler():
    pass


def detect_intel_compiler(compiler_exe="icx"):
    pass


def detect_suncc_compiler(compiler_exe="cc"):
    pass


def detect_clang_compiler(compiler_exe="clang"):
    pass


def detect_msvc_compiler():
    pass


def detect_cl_compiler(compiler_exe="cl"):
    """ only if CC/CXX env-vars are defined pointing to cl.exe, and the VS environment must
    be active to have them in the path
    """
    pass


def detect_emcc_compiler(compiler_exe="emcc"):
    pass


def default_compiler_version(compiler, version):
    """ returns the default version that Conan uses in profiles, typically dropping some
    of the minor or patch digits, that do not affect binary compatibility
    """
    pass


def detect_sdk_version(sdk):
    pass
