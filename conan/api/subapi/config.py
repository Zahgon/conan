import os

from conan.api.output import ConanOutput

from conan.internal.cache.home_paths import HomePaths
from conan.internal.graph.graph import CONTEXT_HOST, RECIPE_VIRTUAL, Node
from conan.internal.graph.graph_builder import DepsGraphBuilder
from conan.internal.graph.profile_node_definer import consumer_definer
from conan.errors import ConanException

from conan.internal.model.conanconfig import loadconanconfig, saveconanconfig, loadconanconfig_yml
from conan.internal.model.conf import BUILT_IN_CONFS
from conan.internal.model.pkg_type import PackageType
from conan.api.model import RecipeReference, Remote
from conan.internal.util.files import rmdir, remove


class ConfigAPI:
    """ This API provides methods to manage the Conan configuration in the Conan home folder.
    It allows installing configurations from various sources, retrieving global configuration
    values, and listing available configurations. It also provides methods to clean the
    Conan home folder, resetting it to a clean state.
    """

    def __init__(self, conan_api, helpers):
        self._conan_api = conan_api
        self._helpers = helpers

    def home(self):
        """ return the current Conan home folder containing the configuration files like
        remotes, settings, profiles, and the packages cache. It is provided for debugging
        purposes. Recall that it is not allowed to write, modify or remove packages in the
        packages cache, and that to automate tasks that uses packages from the cache Conan
        provides mechanisms like deployers or custom commands.
        """
        pass

    def install(self, path_or_url: str, verify_ssl, config_type=None, args=None,
                source_folder=None, target_folder=None) -> None:
        """ install Conan configuration from a git repo, from a zip file in an http server
        or a local folder

        Calling this method will cause a reinitilization of the full ConanAPI, with possible
        invalidation of cached information, and references to objects from the ConanAPI might
        become dangling or outdated.

        :param path_or_url: path or url to install. It can be a http://.../somefile.zip, a
            git repository URL, or a local folder
        :param verify_ssl: Argument passed to python-requests library for SSL verification
        :param config_type: type of configuration to install: "git", "dir", "file", "url"
        :param args: additional arguments to pass to git repositories cloning
        :param source_folder: If specified, install files from that folder of the origin only
        :param target_folder: If the files are to be installed in a specific folder in the Conan
            home. For example, if it is desired to install only profiles from a configuration and
            using source_folder="profiles", it might be expected to use target_folder="profiles"
            to keep the correct profile files location in the local home.
        """
        pass

    def install_package(self, require, lockfile=None, force=False, remotes=None, profile=None):
        """ install Conan configuration from a Conan package

        Calling this method will cause a reinitilization of the full ConanAPI, with possible
        invalidation of cached information, and references to objects from the ConanAPI might
        become dangling or outdated.

        :param require: The package requirement to be installed. It can contain version range
            expressions. If the revision is not specified, as a recipe ``requires``, it will
            also resolve to the latest recipe-revision
        :param lockfile: Lockfile to be used to constrain and lock the versions and recipe-revisions
            from the input requirements, to the exact versions and revisions specified in the
            lockfile
        :param force: If the package has already been installed, nothing will be done unless
            force is True
        :param remotes: Remotes to look for the configuration package
        :param profile: If specified, use that profile to resolve for profile-specific different
            configurations, like depending on different settings.
        :return: list of RecipeReferences of the installed configuration packages
        """
        pass

    @staticmethod
    def load_conanconfig(path, remotes):
        # Internal, do not document yet.
        pass

    def install_conanconfig(self, path, lockfile=None, force=False, remotes=None, profile=None):
        """ install Conan configuration from a Conan "conanconfig.yml" file

        Calling this method will cause a reinitilization of the full ConanAPI, with possible
        invalidation of cached information, and references to objects from the ConanAPI might
        become dangling or outdated.

        :param path: Path to the conanconfig.yml file containing the configuration packages
            requirement definitions
        :param lockfile: Lockfile to be used to constrain and lock the versions and recipe-revisions
            from the input requirements, to the exact versions and revisions specified in the
            lockfile
        :param force: If the package has already been installed, nothing will be done unless
            force is True
        :param remotes: Remotes to look for the configuration package
        :param profile: If specified, use that profile to resolve for profile-specific different
            configurations, like depending on different settings.
        :return: list of RecipeReferences of the installed configuration packages
        """
        pass

    def _install_pkgs(self, required_pkgs, force):
        pass

    def fetch_packages(self, requires, lockfile=None, remotes=None, profile=None):
        """ get and download configuration packages into the Conan cache, without installing
        such configuration in the current Conan home.

        This shouldn't be necessary for regular Conan configuration, and used at the moment
        exclusively for the "conan lock upgrade-config" experimental command.
        """
        pass

    def get(self, name, default=None, check_type=None):
        """ get the value of a global.conf item

        :param name: configuration value to return
        :param default: default value to return if the configuration doesn't contain a value
        :param check_type: check if value is of type check_type, only if the value is defined
        """
        return self._helpers.global_conf.get(name, default=default, check_type=check_type)

    def show(self, pattern) -> dict:
        """ get the values of global.conf for those configurations that matches the pattern
        that have an actual user definition.

        Values with no user definitions will be skipped from the returned value,
        defaults for those confs won't be shown.

        :param pattern: pattern to match against
        :return: dict of configuration values
        """
        pass

    @staticmethod
    def conf_list() -> dict:
        """ list all the available built-in configurations

        :return: A sorted dictionary with all possible built-in configurations
        """
        pass

    def clean(self) -> None:
        """ reset the Conan home folder to a clean state, removing all the user
        custom configuration, custom files, and resetting modified files
        """
        pass

    @property
    def settings_yml(self):
        """ Get the contents of the settings.yml and user_settings.yml files,
        which define the possible values for settings.

        Note that this is different from the settings present in a conanfile,
        which represent the actual values for a specific package, while this
        property represents the possible values for each setting.

        This is intended to be a **read-only** value, do not try to attempt to modify,
        inject or remove settings with this attribute.

        :returns: A read-only object representing the settings scheme, with a
            ``possible_values()`` method that returns a dictionary with the possible
            values for each setting, and a ``fields`` property that returns an ordered
            list with the fields of each setting.
            Note that it's possible to access nested settings using attribute access,
            such as ``settings_yml.compiler.possible_values()``.
        """
        pass
