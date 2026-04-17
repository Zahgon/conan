import os

from conan.api.output import ConanOutput
from conan.cli import make_abs_path
from conan.internal.graph.graph import Overrides
from conan.errors import ConanException
from conan.internal.model.lockfile import Lockfile, LOCKFILE


class LockfileAPI:

    def __init__(self, conan_api):
        self._conan_api = conan_api

    @staticmethod
    def get_lockfile(lockfile=None, conanfile_path=None, cwd=None, partial=False,
                     overrides=None) -> Lockfile:
        """ obtain a lockfile, following this logic:

        If lockfile is explicitly defined, it would be either absolute or relative to cwd and
        the lockfile file must exist. If lockfile="" (empty string) the default "conan.lock"
        lockfile will not be automatically used even if it is present.

        If lockfile is not defined, it will still look for a default conan.lock:

         - if conanfile_path is defined, it will be besides it
         - if conanfile_path is not defined, the default conan.lock should be in cwd
         - if the default conan.lock cannot be found, it is not an error


        :param partial: If the obtained lockfile will allow partial resolving
        :param cwd: the current working dir, if None, os.getcwd() will be used
        :param conanfile_path: The full path to the conanfile, if existing
        :param lockfile: the name of the lockfile file
        :param overrides: Dictionary of overrides {overriden: [new_ref1, new_ref2]}
        """
        pass

    def update_lockfile_export(self, lockfile, conanfile, ref, is_build_require=False):
        # The package_type is not fully processed at export
        pass

    @staticmethod
    def update_lockfile(lockfile, graph, lock_packages=False, clean=False):
        pass

    @staticmethod
    def merge_lockfiles(lockfiles):
        pass

    @staticmethod
    def add_lockfile(lockfile=None, requires=None, build_requires=None, python_requires=None,
                     config_requires=None):
        pass

    @staticmethod
    def remove_lockfile(lockfile, requires=None, build_requires=None, python_requires=None,
                        config_requires=None):
        pass

    @staticmethod
    def save_lockfile(lockfile, lockfile_out, path=None):
        pass
