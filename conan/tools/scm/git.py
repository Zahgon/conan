import fnmatch
import os

from conan.api.output import Color
from conan.tools.files import chdir, update_conandata
from conan.errors import ConanException
from conan.internal.model.conf import ConfDefinition
from conan.internal.util.files import mkdir
from conan.internal.util.runners import check_output_runner


class Git:
    """
    Git is a wrapper for several common patterns used with *git* tool.
    """
    def __init__(self, conanfile, folder=".", excluded=None):
        """
        :param conanfile: Conanfile instance.
        :param folder: Current directory, by default ``.``, the current working directory.
        :param excluded: Files to be excluded from the "dirty" checks. It will compose with the
          configuration ``core.scm:excluded`` (the configuration has higher priority).
          It is a list of patterns to ``fnmatch``.
        """
        self._conanfile = conanfile
        self.folder = folder
        self._excluded = excluded
        global_conf = conanfile._conan_helpers.global_conf  # noqa _conan_helpers
        conf_excluded = global_conf.get("core.scm:excluded", check_type=list)
        if conf_excluded:
            if excluded:
                c = ConfDefinition()
                c.loads(f"core.scm:excluded={excluded}")
                c.update_conf_definition(global_conf)
                self._excluded = c.get("core.scm:excluded", check_type=list)
            else:
                self._excluded = conf_excluded
        self._local_url = global_conf.get("core.scm:local_url", choices=["allow", "block"])

    def run(self, cmd, hidden_output=None):
        """
        Executes ``git <cmd>``

        :return: The console output of the command.
        """
        pass

    def get_commit(self, repository=False):
        """
        :param repository: By default gets the commit of the defined folder, use repo=True to get
                     the commit of the repository instead.
        :return: The current commit, with ``git rev-list HEAD -n 1 -- <folder>``.
            The latest commit is returned, irrespective of local not committed changes.
        """
        pass

    def get_remote_url(self, remote="origin"):
        """
        Obtains the URL of the remote git remote repository, with ``git remote -v``

        **Warning!**
        Be aware that This method will get the output from ``git remote -v``.
        If you added tokens or credentials to the remote in the URL, they will be exposed.
        Credentials shouldn’t be added to git remotes definitions, but using a credentials manager
        or similar mechanism. If you still want to use this approach, it is your responsibility
        to strip the credentials from the result.

        :param remote: Name of the remote git repository ('origin' by default).
        :return: URL of the remote git remote repository.
        """
        pass

    def commit_in_remote(self, commit, remote="origin"):
        """
        Checks that the given commit exists in the remote, with ``branch -r --contains <commit>``
        and checking an occurrence of a branch in that remote exists.

        :param commit: Commit to check.
        :param remote: Name of the remote git repository ('origin' by default).
        :return: True if the given commit exists in the remote, False otherwise.
        """
        pass

    def is_dirty(self, repository=False):
        """
        Returns if the current folder is dirty, running ``git status -s``
        The ``Git(..., excluded=[])`` argument and the ``core.scm:excluded`` configuration will
        define file patterns to be skipped from this check.

        :param repository: By default checks if the current folder is dirty. If repository=True
                     it will check the root repository folder instead, not the current one.
        :return: True, if the current folder is dirty. Otherwise, False.
        """
        pass

    def get_url_and_commit(self, remote="origin", repository=False):
        """
        This is an advanced method, that returns both the current commit, and the remote repository url.
        This method is intended to capture the current remote coordinates for a package creation,
        so that can be used later to build again from sources from the same commit. This is the behavior:

        * If the repository is dirty, it will raise an exception. Doesn’t make sense to capture coordinates
          of something dirty, as it will not be reproducible. If there are local changes, and the
          user wants to test a local conan create, should commit the changes first (locally, not push the changes).

        * If the repository is not dirty, but the commit doesn’t exist in the given remote, the method
          will return that commit and the URL of the local user checkout. This way, a package can be
          conan create created locally, testing everything works, before pushing some changes to the remote.

        * If the repository is not dirty, and the commit exists in the specified remote, it will
          return that commit and the url of the remote.

        **Warning!**
        Be aware that This method will get the output from ``git remote -v``.
        If you added tokens or credentials to the remote in the URL, they will be exposed.
        Credentials shouldn’t be added to git remotes definitions, but using a credentials manager
        or similar mechanism. If you still want to use this approach, it is your responsibility
        to strip the credentials from the result.

        :param remote: Name of the remote git repository ('origin' by default).
        :param repository: By default gets the commit of the defined folder, use repo=True to get
                     the commit of the repository instead.
        :return: (url, commit) tuple
        """
        pass

    def get_repo_root(self):
        """
        Get the current repository top folder with ``git rev-parse --show-toplevel``

        :return: Repository top folder.
        """
        pass

    def clone(self, url, target="", args=None, hide_url=True):
        """
        Performs a ``git clone <url> <args> <target>`` operation, where target is the target directory.

        :param url: URL of remote repository.
        :param target: Target folder.
        :param args: Extra arguments to pass to the git clone as a list.
        :param hide_url: Hides the URL from the log output to prevent accidental
                     credential leaks. Can be disabled by passing ``False``.
        """
        pass

    def fetch_commit(self, url, commit, hide_url=True):
        """
        Experimental: does a single commit fetch and checkout, instead of a full clone,
        should be faster.

        :param url: URL of remote repository.
        :param commit: The commit ref to checkout.
        :param hide_url: Hides the URL from the log output to prevent accidental
                     credential leaks. Can be disabled by passing ``False``.
        """
        pass

    def checkout(self, commit):
        """
        Checkouts the given commit using ``git checkout <commit>``.

        :param commit: Commit to checkout.
        """
        pass

    def included_files(self):
        """
        Run ``git ls-files --full-name --others --cached --exclude-standard`` to the get the list
            of files not ignored by ``.gitignore``

        :return: List of files.
        """
        pass

    def coordinates_to_conandata(self, repository=False):
        """
        Capture the "url" and "commit" from the Git repo, calling ``get_url_and_commit()``, and then
        store those in the ``conandata.yml`` under the "scm" key. This information can be
        used later to clone and checkout the exact source point that was used to create this
        package, and can be useful even if the recipe uses ``exports_sources`` as mechanism to
        embed the sources.

        :param repository: By default gets the commit of the defined folder, use repository=True to get
                     the commit of the repository instead.
        """
        pass

    def checkout_from_conandata_coordinates(self):
        """
        Reads the "scm" field from the ``conandata.yml``, that must contain at least "url" and
        "commit" and then do a ``clone(url, target=".")``, ``fetch <commit>``, followed by a ``checkout(commit)``.
        """
        pass
