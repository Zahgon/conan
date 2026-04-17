import os
from contextlib import contextmanager

from conan.internal.model.manifest import FileTreeManifest
from conan.internal.paths import CONANFILE, DATA_YML
from conan.internal.util.files import set_dirty, clean_dirty, is_dirty, rmdir


# To be able to change them later to something shorter
SRC_FOLDER = "s"
BUILD_FOLDER = "b"
PACKAGES_FOLDER = "p"
FINALIZE_FOLDER = "f"
EXPORT_FOLDER = "e"
EXPORT_SRC_FOLDER = "es"
DOWNLOAD_EXPORT_FOLDER = "d"
METADATA = "metadata"


class LayoutBase:
    def __init__(self, ref, base_folder):
        self.reference = ref
        self._base_folder = base_folder

    @property
    def base_folder(self):
        pass

    def remove(self):
        pass


class BasicLayout(LayoutBase):
    # For editables and platform_requires

    def __init__(self, ref, base_folder, editable_output_folder=None):
        super().__init__(ref, base_folder)
        self.editable_output_folder = editable_output_folder

    def conanfile(self):
        # the full conanfile path (including other other.py names) for editables
        # None for platform_requires
        pass

    def metadata(self):
        pass


class RecipeLayout(LayoutBase):

    @contextmanager
    def conanfile_write_lock(self, output):
        pass

    def export(self):
        pass

    def export_sources(self):
        pass

    def metadata(self):
        pass

    def download_export(self):
        pass

    def source(self):
        pass

    def conanfile(self):
        pass

    def conandata(self):
        pass

    def recipe_manifests(self):
        # Used for comparison and integrity check
        pass

    def sources_remove(self):
        pass


class PackageLayout(LayoutBase):

    def __init__(self, ref, base_folder):
        super().__init__(ref, base_folder)
        self.build_id = None

    # TODO: cache2.0 locks implementation
    @contextmanager
    def package_lock(self):
        pass

    def build(self):
        pass

    def package(self):
        pass

    def finalize(self):
        pass

    def download_package(self):
        pass

    def metadata(self):
        pass

    def package_manifests(self):
        pass

    @contextmanager
    def set_dirty_context_manager(self):
        pass

    # TODO: cache2.0 check this
    def package_is_dirty(self):
        pass

    def build_remove(self):
        pass

    # TODO: cache2.0 locks
    def package_remove(self):
        # Here we could validate and check we own a write lock over this package
        pass
