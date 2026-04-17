from pathlib import Path

from conan.internal.graph.graph import CONTEXT_BUILD


class ConanFileInterface:
    """
    This is just a protective wrapper to give consumers
    a limited view of conanfile dependencies, "read" only,
    and only to some attributes, not methods
    """

    def __str__(self):
        return str(self._conanfile)

    def __init__(self, conanfile):
        self._conanfile = conanfile

    def __eq__(self, other):
        """
        The conanfile is a different entity per node, and conanfile equality is identity
        :type other: ConanFileInterface
        """
        return self._conanfile == other._conanfile

    def __hash__(self):
        return hash(self._conanfile)

    @property
    def options(self):
        pass

    @property
    def recipe_folder(self):
        pass

    @property
    def recipe_metadata_folder(self):
        pass

    @property
    def package_folder(self):
        pass

    @property
    def immutable_package_folder(self):
        pass

    @property
    def package_metadata_folder(self):
        pass

    @property
    def package_path(self) -> Path:
        pass

    @property
    def ref(self):
        pass

    @property
    def pref(self):
        pass

    @property
    def buildenv_info(self):
        pass

    @property
    def runenv_info(self):
        pass

    @property
    def cpp_info(self):
        pass

    @property
    def settings(self):
        pass

    @property
    def settings_build(self):
        pass

    @property
    def context(self):
        pass

    @property
    def conf_info(self):
        pass

    @property
    def generator_info(self):
        pass

    @property
    def dependencies(self):
        pass

    @property
    def folders(self):
        pass

    @property
    def is_build_context(self):
        pass

    @property
    def package_type(self):
        pass

    @property
    def languages(self):
        pass

    @property
    def info(self):
        pass

    def set_deploy_folder(self, deploy_folder):
        pass

    @property
    def conan_data(self):
        pass

    @property
    def license(self):
        pass

    @property
    def description(self):
        pass

    @property
    def author(self):
        pass

    @property
    def homepage(self):
        pass

    @property
    def url(self):
        pass

    @property
    def extension_properties(self):
        pass

    @property
    def recipe(self) -> str:
        # IMPORTANT: this should be used only for "informational" purposes, see GH#18996.
        pass

    @property
    def conf(self):
        pass
