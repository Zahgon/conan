import io
import os
import time

from conan.api.output import ConanOutput, TimedOutput
from conan.internal.rest import response_to_str
from conan.internal.errors import InternalErrorException, RequestErrorException, AuthenticationException, \
    ForbiddenException, NotFoundException
from conan.errors import ConanException
from conan.internal.util.files import sha1sum


class FileUploader:

    def __init__(self, requester, verify, config, source_credentials=None):
        self._requester = requester
        self._config = config
        self._verify_ssl = verify
        self._source_credentials = source_credentials

    @staticmethod
    def _handle_400_response(response, auth):
        pass

    def _dedup(self, url, headers, auth):
        """ send the headers to see if it is possible to skip uploading the file, because it
        is already in the server. Artifactory support file deduplication
        """
        pass

    def exists(self, url, auth):
        response = self._requester.head(url, verify=self._verify_ssl, auth=auth,
                                        source_credentials=self._source_credentials)
        return bool(response.ok)

    def upload(self, url, abs_path, auth=None, dedup=False, retry=None, retry_wait=None,
               ref=None):
        pass

    def _upload_file(self, url, abs_path, headers, auth, ref):
        pass


class FileProgress(io.FileIO):
    def __init__(self, path: str, msg: str = "Uploading", interval: float = 10, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self._size = os.path.getsize(path)
        self._filename = os.path.basename(path)
        # Report only on big sizes (>100MB)
        self._reporter = TimedOutput(interval=interval) if self._size > 100_000_000 else None
        self._bytes_read = 0
        self.msg = msg

    def read(self, size: int = -1) -> bytes:
        pass
