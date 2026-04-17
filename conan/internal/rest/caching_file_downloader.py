import os
import shutil

from urllib.parse import urlparse
from urllib.request import url2pathname

from conan.api.output import ConanOutput
from conan.internal.cache.home_paths import HomePaths
from conan.internal.rest.file_downloader import FileDownloader
from conan.internal.rest.download_cache import DownloadCache
from conan.internal.errors import AuthenticationException, ForbiddenException, NotFoundException
from conan.errors import ConanException
from conan.internal.util.files import mkdir, set_dirty_context_manager, remove_if_dirty, human_size


class SourcesCachingDownloader:
    """ Class for downloading recipe download() urls
    if the config is active, it can use caching/backup-sources
    """
    def __init__(self, conanfile):
        helpers = getattr(conanfile, "_conan_helpers")
        self._global_conf = helpers.global_conf
        self._file_downloader = FileDownloader(helpers.requester, scope=conanfile.display_name,
                                               source_credentials=True)
        self._home_folder = helpers.home_folder
        self._output = conanfile.output
        self._conanfile = conanfile

    def download(self, urls, file_path,
                 retry, retry_wait, verify_ssl, auth, headers, md5, sha1, sha256):
        pass

    def _caching_download(self, urls, file_path,
                          retry, retry_wait, verify_ssl, auth, headers, md5, sha1, sha256,
                          download_cache_folder, backups_urls):
        """
        this download will first check in the local cache, if not there, it will go to the list
        of backup_urls defined by user conf (by default ["origin"]), and iterate it until
        something is found.
        """
        pass

    def _origin_download(self, urls, cached_path, retry, retry_wait,
                         verify_ssl, auth, headers, md5, sha1, sha256, is_last):
        """ download from the internet, the urls provided by the recipe (mirrors).
        """
        pass

    def _backup_download(self, backup_url, backups_urls, sha256, cached_path, urls, is_last):
        """ download from a Conan backup sources file server, like an Artifactory generic repo
        All failures are bad, except NotFound. The server must be live, working and auth, we
        don't want silently skipping a backup because it is down.
        """
        pass

    def _download_from_urls(self, urls, file_path, retry, retry_wait, verify_ssl, auth, headers,
                            md5, sha1, sha256):
        """ iterate the recipe provided list of urls (mirrors, all with same checksum) until
        one succeed
        """
        pass


class ConanInternalCacheDownloader:
    """ This is used for the download of Conan packages from server, not for sources/backup sources
    """
    def __init__(self, requester, config, scope=None):
        self._download_cache = config.get("core.download:download_cache")
        if self._download_cache and not os.path.isabs(self._download_cache):
            raise ConanException("core.download:download_cache must be an absolute path")
        self._file_downloader = FileDownloader(requester, scope=scope)
        self._scope = scope

    def download(self, url, file_path, auth, verify_ssl, retry, retry_wait, metadata=False):
        pass
