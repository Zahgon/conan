import os
import tempfile

from conan.internal.graph.graph import RECIPE_CONSUMER, RECIPE_EDITABLE
from conan.errors import ConanException


def cmake_layout(conanfile, generator=None, src_folder=".", build_folder="build"):
    """
    :param conanfile: The current recipe object. Always use ``self``.
    :param generator: Allow defining the CMake generator. In most cases it doesn't need to be passed,
                      as it will get the value from the configuration
                      ``tools.cmake.cmaketoolchain:generator``, or it will automatically deduce
                      the generator from the ``settings``
    :param src_folder: Value for ``conanfile.folders.source``, change it if your source code
                       (and CMakeLists.txt) is in a subfolder.
    :param build_folder: Specify the name of the "base" build folder. The default is "build", but
                        if that folder name is used by the project, a different one can be defined
    """
    pass


def get_build_folder_custom_vars(conanfile):
    pass
