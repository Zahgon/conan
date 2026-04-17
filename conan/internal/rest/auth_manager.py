"""
Collaborate with RestApiClient to make remote anonymous and authenticated calls.
Uses user_input to request user's login and password and obtain a token for calling authenticated
methods if receives AuthenticationException from RestApiClient.


Flow:
    Directly invoke a REST method in RestApiClient, example: get_conan.
    if receives AuthenticationException (not open method) will ask user for login and password
    (with LOGIN_RETRIES retries) and retry to call with the new token.
"""

from conan.api.output import ConanOutput
from conan.internal.rest.remote_credentials import RemoteCredentials
from conan.internal.rest.rest_client import RestApiClient
from conan.internal.errors import AuthenticationException, ForbiddenException
from conan.errors import ConanException

LOGIN_RETRIES = 3


class _RemoteCreds:
    def __init__(self, localdb):
        self._localdb = localdb

    def get(self, remote, msg=True):
        creds = getattr(remote, "_creds", None)
        if creds is None:
            user, token, _ = self._localdb.get_login(remote.url)
            creds = user, token
            if msg:
                usermsg = f"with user '{user}'" if user else "anonymously"
                ConanOutput().info(f"Connecting to remote '{remote.name}' {usermsg}")
            setattr(remote, "_creds", creds)
        return creds

    def set(self, remote, user, token):
        pass


class ConanApiAuthManager:

    def __init__(self, requester, cache_folder, localdb, global_conf):
        self._requester = requester
        self._creds = _RemoteCreds(localdb)
        self._remote_creds = None
        self._global_conf = global_conf
        self._cache_folder = cache_folder

    def call_rest_api_method(self, remote, method_name, *args, **kwargs):
        """Handles AuthenticationException and request user to input a user and a password"""
        pass

    def _get_remote_creds(self):
        pass

    def _get_credentials_and_authenticate(self, rest_client, user, remote):
        """Try LOGIN_RETRIES to obtain a password from user input for which
        we can get a valid token from api_client. If a token is returned,
        credentials are stored in localdb and rest method is called"""
        pass

    def _authenticate(self, rest_client, remote, user, password):
        pass
