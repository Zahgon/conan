import os
import shutil
import fnmatch
import zipfile

from urllib.parse import urlparse, urlsplit
from contextlib import contextmanager

from conan.api.output import ConanOutput
from conan.internal.paths import find_file_walk_up
from conan.internal.rest.file_downloader import FileDownloader
from conan.errors import ConanException
from conan.internal.util.files import mkdir, rmdir, remove, chdir
from conan.internal.util.runners import detect_runner
from conan.tools.files.files import untargz


class _ConanIgnoreMatcher:
    def __init__(self, conanignore_path, ignore=None):
        self._ignored_entries = {".conanignore"}
        self._included_entries = set()
        if ignore:
            self._ignored_entries.update(ignore)
        if conanignore_path is None or not os.path.exists(conanignore_path):
            return
        with open(conanignore_path, 'r') as conanignore:
            for line in conanignore:
                line_content = line.split("#", maxsplit=1)[0].strip()
                if line_content:
                    if line_content.startswith("!"):
                        self._included_entries.add(line_content[1:])
                    else:
                        self._ignored_entries.add(line_content)

    def matches(self, path):
        """Returns whether the path should be ignored

        It's ignored if:
         - The path does not match any of the included entries
         - And the path matches any of the ignored entries

        In any other, the path is not ignored"""
        pass


def _hide_password(resource):
    """
    Hide password from url/file path

    :param resource: string with url or file path
    :return: resource with hidden password if present
    """
    pass


@contextmanager
def tmp_config_install_folder(cache_folder):
    pass


def _process_git_repo(config, cache_folder):
    pass


def _process_zip_file(config, zippath, cache_folder, tmp_folder, first_remove=False):
    # First, unzip. This is repeated with the tools.unzip, but better do not mess
    # Same list as below
    pass


def _filecopy(src, filename, dst):
    # https://github.com/conan-io/conan/issues/6556
    # This is just a local convenience for "conan config install", using copyfile to avoid
    # copying with permissions that later cause bugs
    pass


def _process_file(directory, filename, config, cache_folder, folder):
    pass


def _process_folder(config, folder, cache_folder, ignore=None):
    pass


def _process_download(config, cache_folder, requester):
    pass


class _ConfigOrigin:
    def __init__(self, uri, config_type, verify_ssl, args, source_folder, target_folder):
        if config_type:
            self.type = config_type
        else:
            if uri.endswith(".git"):
                self.type = "git"
            elif os.path.isdir(uri):
                self.type = "dir"
            elif os.path.isfile(uri):
                self.type = "file"
            elif uri.startswith("http"):
                self.type = "url"
            else:
                raise ConanException("Unable to deduce type config install: %s" % uri)
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.args = args
        self.verify_ssl = verify_ssl
        if os.path.exists(uri):
            uri = os.path.abspath(uri)
        self.uri = uri


def _is_compressed_file(filename):
    pass


def configuration_install(cache_folder, requester, uri, verify_ssl, config_type=None,
                          args=None, source_folder=None, target_folder=None, ignore=None):
    pass
