import fnmatch
import json
import os
from collections import OrderedDict
from urllib.parse import urlparse

from conan.api.model import Remote, LOCAL_RECIPES_INDEX
from conan.api.output import ConanOutput
from conan.internal.cache.home_paths import HomePaths
from conan.internal.rest.remote_credentials import RemoteCredentials
from conan.internal.rest.rest_client_local_recipe_index import add_local_recipes_index_remote, \
    remove_local_recipes_index_remote
from conan.internal.api.remotes.localdb import LocalDB
from conan.errors import ConanException
from conan.internal.util.files import save, load

CONAN_CENTER_REMOTE_NAME = "conancenter"


class RemotesAPI:
    """ The ``RemotesAPI`` manages the definition of remotes, contained in the "remotes.json" file
    in the Conan home, supporting addition, removal, update, rename, enable, disable of remotes.
    These operations do not contact the servers or check their existence at all. If they are not
    available, they will fail later when used.

    The ``user_xxx`` methods perform authentication related tasks, and some of them will contact
    the servers to perform such authentication
    """

    def __init__(self, conan_api, api_helpers):
        # This method is private, the subapi is not instantiated by users
        self._conan_api = conan_api
        self._api_helpers = api_helpers
        self._home_folder = conan_api.home_folder
        self._remotes_file = HomePaths(self._home_folder).remotes_path

    def list(self, pattern=None, only_enabled=True):
        """
        Obtain a list of :ref:`Remote <conan.api.model.Remote>` objects matching the pattern.

        :param pattern: ``None``, single ``str`` or list of ``str``. If it is ``None``,
          all remotes will be returned (equivalent to ``pattern="*"``).
        :param only_enabled: boolean, by default return only enabled remotes
        :return: A list of :ref:`Remote <conan.api.model.Remote>` objects

        """
        pass

    def disable(self, pattern):
        """
        Disable all remotes matching ``pattern``

        :param pattern: single ``str`` or list of ``str``. If the pattern is an exact name without
          wildcards like "*" and no remote is found matching that exact name, it will raise an error.
        :return: the list of disabled :ref:`Remote <conan.api.model.Remote>` objects  (even if they
          were already disabled)
        """
        pass

    def enable(self, pattern):
        """
        Enable all remotes matching ``pattern``.

        :param pattern: single ``str`` or list of ``str``. If the pattern is an exact name without
          wildcards like "*" and no remote is found matching that exact name, it will raise an error.
        :return: the list of enabled :ref:`Remote <conan.api.model.Remote>` objects (even if they
          were already enabled)
        """
        pass

    def get(self, remote_name):
        """
        Obtain a :ref:`Remote <conan.api.model.Remote>` object

        :param remote_name: the exact name of the remote to be returned
        :return: the :ref:`Remote <conan.api.model.Remote>` object, or raise an Exception if the
          remote does not exist.
        """
        remotes = _load(self._remotes_file)
        try:
            return {r.name: r for r in remotes}[remote_name]
        except KeyError:
            raise ConanException(f"Remote '{remote_name}' doesn't exist")

    def add(self, remote: Remote, force=False, index=None):
        """
        Add a new :ref:`Remote <conan.api.model.Remote>` object to the existing ones


        :param remote: a :ref:`Remote <conan.api.model.Remote>` object to be added
        :param force: do not fail if the remote already exist (but default it fails)
        :param index: if not defined, the new remote will be last one. Pass an integer to insert
          the remote in that position instead of the last one
        """
        pass

    def remove(self, pattern):
        """
        Remove the remotes matching the ``pattern``

        :param pattern: single ``str`` or list of ``str``. If the pattern is an exact name without
          wildcards like "*" and no remote is found matching that exact name, it will raise an error.
        :return: The list of removed :ref:`Remote <conan.api.model.Remote>` objects
        """
        pass

    def update(self, remote_name: str, url=None, secure=None, disabled=None, index=None,
               allowed_packages=None, recipes_only=None):
        """
        Update an existing remote

        :param remote_name: The name of the remote to update, must exist
        :param url: optional url to update, if not defined it will not be updated
        :param secure:  optional ssl secure connection to update
        :param disabled: optional disabled state
        :param index:  optional integer to change the order of the remote
        :param allowed_packages: optional list of packages allowed from this remote
        :param recipes_only: optional boolean to only allow recipe downloads from this remote,
            never package binaries
        """
        remotes = _load(self._remotes_file)
        try:
            remote = {r.name: r for r in remotes}[remote_name]
        except KeyError:
            raise ConanException(f"Remote '{remote_name}' doesn't exist")
        if url is not None:
            if remote.remote_type != LOCAL_RECIPES_INDEX:
                _validate_url(url)
            _check_urls(remotes, url, force=False, current=remote)
            remote.url = url
        if secure is not None:
            remote.verify_ssl = secure
        if disabled is not None:
            remote.disabled = disabled
        if allowed_packages is not None:
            remote.allowed_packages = allowed_packages
        if recipes_only is not None:
            remote.recipes_only = recipes_only

        if index is not None:
            remotes = [r for r in remotes if r.name != remote.name]
            remotes.insert(index, remote)
        _save(self._remotes_file, remotes)

    def rename(self, remote_name: str, new_name: str):
        """
        Change the name of an existing remote

        :param remote_name: The previous existing name
        :param new_name: The new name
        """
        pass

    def user_info(self, remote: Remote):
        # TODO: Review
        pass

    def user_login(self, remote: Remote, username: str, password: str):
        """
        Perform user authentication against the given remote with the provided username and password

        :param remote: a :ref:`Remote <conan.api.model.Remote>` object
        :param username: the user login as ``str``
        :param password: password ``str``
        """
        pass

    def login(self, remotes, username=None, password=None):
        pass

    def user_logout(self, remote: Remote):
        """
        Logout from the given :ref:`Remote <conan.api.model.Remote>`

        :param remote: The :ref:`Remote <conan.api.model.Remote>` object to logout
        """
        pass

    def user_set(self, remote: Remote, username):
        # TODO: Review
        pass

    def user_auth(self, remote: Remote, with_user=False, force=False):
        # TODO: Review
        pass


def _load(remotes_file):
    pass


def _save(remotes_file, remotes):
    pass


def _filter(remotes, pattern, only_enabled=True):
    pass


def _validate_url(url):
    """ Check if URL contains protocol and address
    :param url: URL to be validated
    """
    pass


def _check_urls(remotes, url, force, current):
    # The remote name doesn't exist
    pass
