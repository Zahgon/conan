import json
import os
import platform

from jinja2 import Template

from conan.api.input import UserInput
from conan.internal.cache.home_paths import HomePaths

from conan.internal.loader import load_python_file
from conan.api.output import ConanOutput
from conan.internal.errors import scoped_traceback
from conan.errors import ConanException
from conan.internal.util.files import load


class RemoteCredentials:
    def __init__(self, cache_folder, global_conf):
        self._global_conf = global_conf
        self._urls = {}
        auth_plugin_path = HomePaths(cache_folder).auth_remote_plugin_path
        self._auth_remote_plugin = _load_auth_remote_plugin(auth_plugin_path)
        creds_path = os.path.join(cache_folder, "credentials.json")
        if not os.path.exists(creds_path):
            return
        try:
            template = Template(load(creds_path))
            content = template.render({"platform": platform, "os": os})
            content = json.loads(content)

            self._urls = {credentials["remote"]: {"user": credentials["user"],
                                                  "password": credentials["password"]}
                          for credentials in content["credentials"]}
        except Exception as e:
            raise ConanException(f"Error loading 'credentials.json' {creds_path}: {repr(e)}")

    def auth(self, remote, user=None):
        # First get the auth_remote_plugin
        pass

    @staticmethod
    def _get_env(remote, user):
        """
        Try get creds from env-vars
        """
        pass


def _load_auth_remote_plugin(auth_remote_plugin_path):
    pass
