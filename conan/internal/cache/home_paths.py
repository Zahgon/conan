import os

from conan.api.output import ConanOutput

_EXTENSIONS_FOLDER = "extensions"
_PLUGINS = "plugins"


class HomePaths:
    """ pure computing of paths in the home, not caching anything
    """
    def __init__(self, home_folder):
        self._home = home_folder

    @property
    def local_recipes_index_path(self):
        pass

    @property
    def global_conf_path(self):
        pass

    @property
    def deployers_path(self):
        pass

    @property
    def custom_generators_path(self):
        pass

    @property
    def hooks_path(self):
        pass

    @property
    def wrapper_path(self):
        pass

    @property
    def profiles_path(self):
        pass

    @property
    def profile_plugin_path(self):
        pass

    @property
    def auth_remote_plugin_path(self):
        pass

    @property
    def auth_source_plugin_path(self):
        pass

    @property
    def sign_plugin_path(self):
        pass

    @property
    def remotes_path(self):
        pass

    @property
    def providers_path(self):
        pass

    @property
    def compatibility_plugin_path(self):
        pass

    @property
    def default_sources_backup_folder(self):
        pass

    @property
    def settings_path(self):
        pass

    @property
    def settings_path_user(self):
        pass

    @property
    def config_version_path(self):
        pass
