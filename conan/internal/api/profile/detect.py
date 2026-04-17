from conan.api.output import ConanOutput
from conan.internal.api.detect.detect_api import detect_os, detect_arch, default_msvc_runtime, \
    detect_libcxx, detect_cppstd, detect_default_compiler, default_compiler_version


def detect_defaults_settings():
    """ try to deduce current machine values without any constraints at all
    :return: A list with default settings
    """
    pass
