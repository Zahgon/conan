import os
import re
import time


from conan.api.output import ConanOutput, TimedOutput
from conan.internal.rest import response_to_str
from conan.internal.errors import (ConanConnectionError, RequestErrorException,
                                   AuthenticationException, ForbiddenException, NotFoundException)
from conan.errors import ConanException
from conan.internal.util.files import human_size, check_with_algorithm_sum


class FileDownloader:

    def __init__(self, requester, scope=None, source_credentials=None):
        self._output = ConanOutput(scope=scope)
        self._requester = requester
        self._source_credentials = source_credentials

    def download(self, url, file_path, retry=2, retry_wait=0, verify_ssl=True, auth=None,
                 overwrite=False, headers=None, md5=None, sha1=None, sha256=None):
        """ in order to make the download concurrent, the folder for file_path MUST exist
        """
        pass

    @staticmethod
    def check_checksum(file_path, md5, sha1, sha256):
        pass

    def _download_file(self, url, auth, headers, file_path, verify_ssl, try_resume=False):
        pass
