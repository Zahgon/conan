import os

from conan.internal.model.cpp_info import CppInfo
from conan.internal.model.conf import Conf


class Infos:

    def __init__(self):
        self.source = CppInfo()
        self.build = CppInfo()
        self.package = CppInfo(set_defaults=True)


class PartialLayout:
    def __init__(self):
        from conan.tools.env import Environment
        self.buildenv_info = Environment()
        self.runenv_info = Environment()
        self.conf_info = Conf()

    def set_relative_base_folder(self, folder):
        pass


class Layouts:
    def __init__(self):
        self.source = PartialLayout()
        self.build = PartialLayout()
        self.package = PartialLayout()


class Folders:

    def __init__(self):
        self._base_source = None
        self._base_build = None
        self._base_package = None
        self._base_generators = None

        self._base_export = None
        self._base_export_sources = None

        self._base_recipe_metadata = None
        self._base_pkg_metadata = None
        self._immutable_package_folder = None

        self.source = ""
        self.build = ""
        self.package = ""
        self.generators = ""
        # Relative location of the project root, if the conanfile is not in that project root, but
        # in a subfolder: e.g: If the conanfile is in a subfolder then self.root = ".."
        self.root = None
        # The relative location with respect to the project root of the subproject containing the
        # conanfile.py, that makes most of the output folders defined in layouts (cmake_layout, etc)
        # start from the subproject again
        self.subproject = None
        self.build_folder_vars = None

    def set_base_folders(self, conanfile_folder, output_folder):
        """ this methods can be used for defining all the base folders in the
        local flow (conan install, source, build), where only the current conanfile location
        and the potential --output-folder user argument are the folders to take into account
        If the "layout()" method defines a self.folders.root = "xxx" it will be used to compute
        the base folder

        @param conanfile_folder: the location where the current consumer conanfile is
        @param output_folder: Can potentially be None (for export-pkg: TODO), in that case
        the conanfile location is used
        """
        pass

    @property
    def source_folder(self):
        pass

    @property
    def base_source(self):
        pass

    def set_base_source(self, folder):
        pass

    @property
    def build_folder(self):
        pass

    @property
    def recipe_metadata_folder(self):
        pass

    def set_base_recipe_metadata(self, folder):
        pass

    @property
    def package_metadata_folder(self):
        pass

    def set_base_pkg_metadata(self, folder):
        pass

    @property
    def base_build(self):
        pass

    def set_base_build(self, folder):
        pass

    @property
    def base_package(self):
        pass

    def set_base_package(self, folder):
        pass

    @property
    def package_folder(self):
        """For the cache, the package folder is only the base"""
        pass

    def set_finalize_folder(self, folder):
        pass

    @property
    def immutable_package_folder(self):
        pass

    @property
    def generators_folder(self):
        pass

    def set_base_generators(self, folder):
        pass

    @property
    def base_export(self):
        pass

    def set_base_export(self, folder):
        pass

    @property
    def base_export_sources(self):
        pass

    def set_base_export_sources(self, folder):
        pass
