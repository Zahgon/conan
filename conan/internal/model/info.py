import hashlib

from conan.errors import ConanException
from conan.internal.model.dependencies import UserRequirementsDict
from conan.api.model import PkgReference
from conan.api.model import RecipeReference
from conan.internal.util.config_parser import TextINIParse


class _VersionRepr:
    """Class to return strings like 1.Y.Z from a Version object"""

    def __init__(self, version):
        self._version = version

    def stable(self):
        pass

    def major(self):
        # This check is to avoid breaking non-integer major versions
        # for legacy reasons. Users are warned against using them
        pass

    def minor(self):
        # This check is to avoid breaking non-integer major versions
        # for legacy reasons. Users are warned against using them
        pass

    def patch(self):
        # This check is to avoid breaking non-integer major versions
        # for legacy reasons. Users are warned against using them
        pass

    def pre(self):
        # This check is to avoid breaking non-integer major versions
        # for legacy reasons. Users are warned against using them
        pass

    @property
    def build(self):
        pass


class RequirementInfo:

    def __init__(self, ref, package_id, default_package_id_mode):
        self._ref = ref
        self._package_id = package_id
        self.name = self.version = self.user = self.channel = self.package_id = None
        self.recipe_revision = None
        self.package_id_mode = default_package_id_mode

        try:
            func_package_id_mode = getattr(self, default_package_id_mode)
        except AttributeError:
            raise ConanException(f"require {self._ref} package_id_mode='{default_package_id_mode}' "
                                 "is not a known package_id_mode")
        else:
            func_package_id_mode()

    def copy(self):
        # Useful for build_id()
        pass

    def pref(self):
        pass

    def dumps(self):
        pass

    def unrelated_mode(self):
        pass

    def semver_mode(self):
        pass

    def full_version_mode(self):
        pass

    def patch_mode(self):
        pass

    def minor_mode(self):
        pass

    def major_mode(self):
        pass

    def full_package_mode(self):
        pass

    def revision_mode(self):
        pass

    def full_mode(self):
        pass

    full_recipe_mode = full_version_mode
    recipe_revision_mode = full_mode  # to not break everything and help in upgrade


class RequirementsInfo(UserRequirementsDict):

    def copy(self):
        # For build_id() implementation
        pass

    def serialize(self):
        pass

    def __bool__(self):
        return bool(self._data)

    def clear(self):
        pass

    def remove(self, *args):
        pass

    @property
    def pkg_names(self):
        pass

    def dumps(self):
        pass

    def unrelated_mode(self):
        pass

    def semver_mode(self):
        pass

    def patch_mode(self):
        pass

    def minor_mode(self):
        pass

    def major_mode(self):
        pass

    def full_version_mode(self):
        pass

    def full_recipe_mode(self):
        pass

    def full_package_mode(self):
        pass

    def revision_mode(self):
        pass

    def full_mode(self):
        pass

    recipe_revision_mode = full_mode  # to not break everything and help in upgrade


class PythonRequiresInfo:

    def __init__(self, refs, default_package_id_mode):
        self._default_package_id_mode = default_package_id_mode
        if refs:
            self._refs = [RequirementInfo(r, None,
                                          default_package_id_mode=mode or default_package_id_mode)
                          for r, mode in sorted(refs.items())]
        else:
            self._refs = None

    def copy(self):
        # For build_id() implementation
        pass

    def serialize(self):
        pass

    def __bool__(self):
        return bool(self._refs)

    def clear(self):
        pass

    def dumps(self):
        pass

    def unrelated_mode(self):
        pass

    def semver_mode(self):
        pass

    def patch_mode(self):
        pass

    def minor_mode(self):
        pass

    def major_mode(self):
        pass

    def full_version_mode(self):
        pass

    def full_recipe_mode(self):
        pass

    def revision_mode(self):
        pass

    def full_mode(self):
        pass

    recipe_revision_mode = full_mode


def load_binary_info(text):
    # This is used for search functionality, search prints info from this file
    pass


class ConanInfo:

    def __init__(self, settings=None, options=None, reqs_info=None, build_requires_info=None,
                 python_requires=None, conf=None, config_version=None):
        self.invalid = None
        self.cant_build = False  # It will set to a str with a reason if the validate_build() fails
        self.settings = settings
        self.settings_target = None  # needs to be explicitly defined by recipe package_id()
        self.options = options
        self.requires = reqs_info
        self.build_requires = build_requires_info
        self.python_requires = python_requires
        self.conf = conf
        self.config_version = config_version
        self.compatibility_delta = None

    def clone(self):
        """ Useful for build_id implementation and for compatibility()
        """
        pass

    def serialize(self):
        pass

    def dumps(self):
        """
        Get all the information contained in settings, options, requires,
        python_requires, build_requires and conf.
        :return: `str` with the result of joining all the information, e.g.,
            `"[settings]\nos=Windows\n[options]\nuse_Qt=True"`
        """
        pass

    def summarize_compact(self):
        pass

    def dump_diff(self, compatible):
        pass

    def package_id(self):
        """
        Get the `package_id` that is the result of applying the has function SHA-1 to the
        `self.dumps()` return.
        :return: `str` the `package_id`, e.g., `"040ce2bd0189e377b2d15eb7246a4274d1c63317"`
        """
        pass

    def clear(self):
        pass

    def validate(self):
        # If the options are not fully defined, this is also an invalid case
        pass
