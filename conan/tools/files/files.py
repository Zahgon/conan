import gzip
import os
import stat
import platform
import shutil
import subprocess
from typing import Optional
from contextlib import contextmanager
from fnmatch import fnmatch
from shutil import which


from conan.internal.rest.caching_file_downloader import SourcesCachingDownloader
from conan.errors import ConanException
from conan.internal.rest.file_uploader import FileProgress
from conan.internal.util.files import rmdir as _internal_rmdir, human_size, check_with_algorithm_sum


def load(conanfile, path, encoding="utf-8"):
    """
    Utility function to load files in one line. It will manage the open and close of the file,
    and load binary encodings. Returns the content of the file.

    :param conanfile: The current recipe object. Always use ``self``.
    :param path: Path to the file to read
    :param encoding: (Optional, Defaulted to ``utf-8``): Specifies the input file text encoding.
    :return: The contents of the file
    """
    pass


def save(conanfile, path, content, append=False, encoding="utf-8"):
    """
    Utility function to save files in one line. It will manage the open and close of the file
    and creating directories if necessary.

    :param conanfile: The current recipe object. Always use ``self``.
    :param path: Path of the file to be created.
    :param content: Content (str or bytes) to be write to the file.
    :param append: (Optional, Defaulted to False): If ``True`` the contents will be appended to the
           existing one.
    :param encoding: (Optional, Defaulted to utf-8): Specifies the output file text encoding.
    """
    pass


def mkdir(conanfile, path):
    """
    Utility functions to create a directory. The existence of the specified directory is checked,
    so mkdir() will do nothing if the directory already exists.

    :param conanfile: The current recipe object. Always use ``self``.
    :param path: Path to the folder to be created.
    """
    pass


def rmdir(conanfile, path):
    pass


def rm(conanfile, pattern, folder, recursive=False, excludes=None):
    """
    Utility functions to remove files matching a ``pattern`` in a ``folder``.

    :param conanfile: The current recipe object. Always use ``self``.
    :param pattern: Pattern that the files to be removed have to match (fnmatch).
    :param folder: Folder to search/remove the files.
    :param recursive: If ``recursive`` is specified it will search in the subfolders.
    :param excludes: (Optional, defaulted to None) A tuple/list of fnmatch patterns or even a
                     single one to be excluded from the remove pattern.
    """
    pass


def get(conanfile, url, md5=None, sha1=None, sha256=None, destination=".", filename="",
        keep_permissions=False, pattern=None, verify=True, retry=None, retry_wait=None,
        auth=None, headers=None, strip_root=False, extract_filter=None, excludes=None):
    """
    High level download and decompressing of a tgz, zip or other compressed format file.
    Just a high level wrapper for download, unzip, and remove the temporary zip file once unzipped.
    You can pass hash checking parameters: ``md5``, ``sha1``, ``sha256``. All the specified
    algorithms will be checked. If any of them doesn't match, it will raise a ``ConanException``.

    :param conanfile: The current recipe object. Always use ``self``.
    :param destination: (Optional defaulted to ``.``) Destination folder
    :param filename: (Optional defaulted to '') If provided, the saved file will have the specified name,
           otherwise it is deduced from the URL
    :param url: forwarded to ``tools.file.download()``.
    :param md5: forwarded to ``tools.file.download()``.
    :param sha1:  forwarded to ``tools.file.download()``.
    :param sha256:  forwarded to ``tools.file.download()``.
    :param keep_permissions:  forwarded to ``tools.file.unzip()``.
    :param pattern: forwarded to ``tools.file.unzip()``.
    :param verify:  forwarded to ``tools.file.download()``.
    :param retry:  forwarded to ``tools.file.download()``.
    :param retry_wait: S forwarded to ``tools.file.download()``.
    :param auth:  forwarded to ``tools.file.download()``.
    :param headers:  forwarded to ``tools.file.download()``.
    :param strip_root: forwarded to ``tools.file.unzip()``.
    :param extract_filter: forwarded to ``tools.file.unzip()``.
    :param excludes: forwarded to ``tools.file.unzip()``.
    """

    if not filename:  # deduce filename from the URL
        url_base = url[0] if isinstance(url, (list, tuple)) else url
        if "?" in url_base or "=" in url_base:
            raise ConanException("Cannot deduce file name from the url: '{}'. Use 'filename' "
                                 "parameter.".format(url_base))
        filename = os.path.basename(url_base)

    download(conanfile, url, filename, verify=verify,
             retry=retry, retry_wait=retry_wait, auth=auth, headers=headers,
             md5=md5, sha1=sha1, sha256=sha256)
    unzip(conanfile, filename, destination=destination, keep_permissions=keep_permissions,
          pattern=pattern, strip_root=strip_root, extract_filter=extract_filter,
          excludes=excludes)
    os.unlink(filename)


def ftp_download(conanfile, host, filename, login='', password='', secure=False):
    """
    Ftp download of a file. Retrieves a file from an FTP server.

    :param conanfile: The current recipe object. Always use ``self``.
    :param host: IP or host of the FTP server.
    :param filename: Path to the file to be downloaded.
    :param login: Authentication login.
    :param password: Authentication password.
    :param secure: Set to True to use FTP over TLS/SSL (FTPS). Defaults to False for regular FTP.
    """
    pass


def download(conanfile, url, filename, verify=True, retry=None, retry_wait=None,
             auth=None, headers=None, md5=None, sha1=None, sha256=None):
    """
    Retrieves a file from a given URL into a file with a given filename. It uses certificates from
    a list of known verifiers for https downloads, but this can be optionally disabled.

    You can pass hash checking parameters: ``md5``, ``sha1``, ``sha256``. All the specified
    algorithms will be checked. If any of them doesn’t match, the downloaded file will be removed
    and it will raise a ``ConanException``.

    :param conanfile: The current recipe object. Always use ``self``.
    :param url: URL to download. It can be a list, which only the first one will be downloaded, and
                the follow URLs will be used as mirror in case of download error.  Files accessible
                in the local filesystem can be referenced with a URL starting with ``file:///``
                followed by an absolute path to a file (where the third ``/`` implies ``localhost``).
    :param filename: Name of the file to be created in the local storage
    :param verify: When False, disables https certificate validation
    :param retry: Number of retries in case of failure. Default is overridden by
           "tools.files.download:retry" conf
    :param retry_wait: Seconds to wait between download attempts. Default is overriden by
           "tools.files.download:retry_wait" conf.
    :param auth: A tuple of user and password to use HTTPBasic authentication
    :param headers: A dictionary with additional headers
    :param md5: MD5 hash code to check the downloaded file
    :param sha1: SHA-1 hash code to check the downloaded file
    :param sha256: SHA-256 hash code to check the downloaded file
    """
    pass


def rename(conanfile, src, dst):
    """
    Utility functions to rename a file or folder src to dst with retrying. ``os.rename()``
    frequently raises “Access is denied” exception on Windows.
    This function renames file or folder using robocopy to avoid the exception on Windows.



    :param conanfile: The current recipe object. Always use ``self``.
    :param src: Path to be renamed.
    :param dst: Path to be renamed to.
    """
    pass


@contextmanager
def chdir(conanfile, newdir):
    """
    This is a context manager that allows to temporary change the current directory in your conanfile

    :param conanfile: The current recipe object. Always use ``self``.
    :param newdir: Directory path name to change the current directory.

    """
    pass


def chmod(conanfile, path: str, read: Optional[bool] = None, write: Optional[bool] = None,
          execute: Optional[bool] = None, recursive: bool = False):
    """Change file or directory permissions cross-platform.

    .. versionadded:: 2.15

    This function is a simple wrapper around the chmod Unix command, but it is cross-platform supported.
    It is indicated to use it instead of os.stat + os.chmod, as it only changes the permissions of the
    directory or file for the owner and avoids issues with the umask.
    On Windows is limited to changing write permission only.

    Parameters
    ----------
    conanfile : object
        The current recipe object. Always use ``self``.
    path : str
        Path to the file or directory whose permissions will be changed.
    read : bool, optional
        If ``True``, the file or directory will be given read permissions for owner user.
        If ``False``, the read permission will be removed.
        If ``None``, the read permission will be left unchanged.
        Defaults to None.
    write : bool, optional
        If ``True``, the file or directory will be given write permissions for owner user.
        If ``False``, the write permission will be removed.
        If ``None``, the file or directory will not be changed.
        Defaults to None.
    execute : bool, optional
        If ``True``, the file or directory will be given execute permissions for owner user.
        If ``False``, the execution permission will be removed.
        If ``None``, the file or directory will not be changed.
        Defaults to None.
    recursive : bool
        If ``True``, the permissions will be applied recursively to all files and directories
        inside the specified directory. If ``False``, only the specified file or directory will
        be changed. Defaults to False.

    Returns
    -------
    None

    Examples
    --------
    .. code-block:: python
        :caption: Add execution permission to a packaged bash script

        from conan.tools.files import chmod
        chmod(self, os.path.join(self.package_folder, "bin", "script.sh"), execute=True)
    """
    pass


def unzip(conanfile, filename, destination=".", keep_permissions=False, pattern=None,
          strip_root=False, extract_filter=None, excludes=None):
    """
    Extract different compressed formats

    :param conanfile: The current recipe object. Always use ``self``.
    :param filename: Path to the compressed file.
    :param destination: (Optional, Defaulted to ``.``) Destination folder (or file for .gz files)
    :param keep_permissions: (Optional, Defaulted to ``False``) Keep the zip permissions.
           WARNING: Can be dangerous if the zip was not created in a NIX system, the bits could
           produce undefined permission schema. Use this option only if you are sure that the zip
           was created correctly.
    :param pattern: (Optional, Defaulted to ``None``) Extract only paths matching the pattern.
           This should be a Unix shell-style wildcard, see fnmatch documentation for more details.
    :param strip_root: (Optional, Defaulted to False) If True, and all the unzipped contents are
           in a single folder it will flat the folder moving all the contents to the parent folder.
    :param extract_filter: (Optional, defaulted to None). When extracting a tar file,
           use the tar extracting filters define by Python in
           https://docs.python.org/3/library/tarfile.html
    :param excludes: (Optional, defaulted to None). When extracting a file,
           exclude paths matching any of the patterns. This should be a Unix shell-style wildcard,
           see fnmatch documentation for more details.
    """
    pass


def untargz(filename, destination=".", pattern=None, strip_root=False, extract_filter=None,
            excludes=None):
    # NOT EXPOSED at `conan.tools.files` but used in tests
    pass


def check_sha1(conanfile, file_path, signature):
    """
    Check that the specified ``SHA-1`` hash of the ``file_path`` matches the actual hash.
    If doesn’t match it will raise a ``ConanException``.

    :param conanfile: Conanfile object.
    :param file_path: Path of the file to check.
    :param signature: Expected SHA-1 hash.
    """
    pass


def check_md5(conanfile, file_path, signature):
    """
    Check that the specified ``MD5`` hash of the ``file_path`` matches the actual hash.
    If doesn’t match it will raise a ``ConanException``.

    :param conanfile: The current recipe object. Always use ``self``.
    :param file_path: Path of the file to check.
    :param signature: Expected MD5 hash.
    """
    pass


def check_sha256(conanfile, file_path, signature):
    """
    Check that the specified ``SHA-256`` hash of the ``file_path`` matches the actual hash.
    If doesn’t match it will raise a ``ConanException``.

    :param conanfile: Conanfile object.
    :param file_path: Path of the file to check.
    :param signature: Expected SHA-256 hash.
    """
    pass


def replace_in_file(conanfile, file_path, search, replace, strict=True, encoding="utf-8"):
    """
    Replace a string ``search`` in the contents of the file ``file_path`` with the string replace.

    :param conanfile: The current recipe object. Always use ``self``.
    :param file_path: File path of the file to perform the replacing.
    :param search: String you want to be replaced.
    :param replace: String to replace the searched string.
    :param strict: (Optional, Defaulted to ``True``) If ``True``, it raises an error if the searched
           string is not found, so nothing is actually replaced.
    :param encoding: (Optional, Defaulted to utf-8): Specifies the input and output files text
           encoding.
    :return: ``True`` if the pattern was found, ``False`` otherwise if `strict` is ``False``.
    """
    pass


def collect_libs(conanfile, folder=None):
    """
    Returns a sorted list of library names from the libraries (files with extensions *.so*, *.lib*,
    *.a* and *.dylib*) located inside the ``conanfile.cpp_info.libdirs`` (by default) or the
    **folder** directory relative to the package folder. Useful to collect not inter-dependent
    libraries or with complex names like ``libmylib-x86-debug-en.lib``.

    For UNIX libraries staring with **lib**, like *libmath.a*, this tool will collect the library
    name **math**.

    :param conanfile: The current recipe object. Always use ``self``.
    :param folder: (Optional, Defaulted to ``None``): String indicating the subfolder name inside
           ``conanfile.package_folder`` where the library files are.
    :return: A list with the library names
    """
    pass


def move_folder_contents(conanfile, src_folder, dst_folder):
    """ replaces the dst_folder contents with the contents of the src_folder, which can be a
    child folder of dst_folder. This is used in the SCM monorepo flow, when it is necessary
    to use one subproject subfolder to replace the whole cloned git repo
    /base-folder                       /base-folder
        /pkg  (src folder)                 /other/<otherfiles>
          /other/<otherfiles>              /pkg/<pkgfiles>
          /pkg/<pkgfiles>                  <files>
          <files>
        /siblings
        <siblingsfiles>
    """
    pass
