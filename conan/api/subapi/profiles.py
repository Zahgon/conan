import os

from conan.api.output import ConanOutput
from conan.internal.cache.home_paths import HomePaths

from conan.internal.loader import load_python_file
from conan.internal.api.profile.profile_loader import ProfileLoader
from conan.internal.errors import scoped_traceback
from conan.errors import ConanException
from conan.internal.model.profile import Profile

DEFAULT_PROFILE_NAME = "default"


class ProfilesAPI:
    """ This ProfilesAPI is used to list, manage and load Conan profiles
    """

    def __init__(self, conan_api, api_helpers):
        self._conan_api = conan_api
        self._api_helpers = api_helpers
        self._home_paths = HomePaths(conan_api.home_folder)

    def get_default_host(self):
        """
        :return: the path to the default "host" profile, either in the cache or as defined
            by the user in configuration
        """
        pass

    def get_default_build(self):
        """
        :return: the path to the default "build" profile, either in the cache or as
            defined by the user in configuration
        """
        pass

    def get_profiles_from_args(self, args):
        pass

    def get_profile(self, profiles, settings=None, options=None, conf=None, cwd=None, context=None):
        """ Computes a Profile as the result of aggregating all the user arguments, first it
        loads the "profiles", composing them in order (last profile has priority), and
        finally adding the individual settings, options (priority over the profiles)

        :param profiles: the list of profiles to load
        :param settings: list of "key=value" settings to define the profile. Patterns allowed as
           "pkg-pattern:key=value"
        :param options: list of "key=value" options. Patterns allowed as "pkg-pattern:key=value"
        :param conf: list of "key=value" configurations. Following "conf" definitions, patterns
           are allowed as "pkg-pattern:key=value", values that are lists or dictionaries might be
           allowed, and configuration operations like ``+=`` for appending are allowed.
        :param cwd: the current working directory. If None, os.getcwd() will be used.
        :param context: the context, "build" or "host" to which this profile belongs
        """
        pass

    def _get_profile(self, profiles, settings, options, conf, cwd, cache_settings,
                     profile_plugin, global_conf, context):
        pass

    def get_path(self, profile, cwd=None, exists=True):
        """
        :return: the resolved path of the given profile name, that could be in the cache,
            or local, depending on the "cwd"
        """
        pass

    def list(self):
        """
        List all the profiles files in the cache

        :return: an alphabetically ordered list of profile files in the default cache location
        """
        pass

    @staticmethod
    def detect():
        """
        Detects a possible default profile.

        The output of this detection is not guaranteed to be complete or stable, it might
        change in future releases, following the same rules as the "conan profile detect" command.

        :return: an automatically detected Profile, with a "best guess" of the system settings
        """
        pass

    def _load_profile_plugin(self):
        pass
