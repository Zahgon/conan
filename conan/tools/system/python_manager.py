import platform
import os
import shutil
import sys

from conan.tools.build import cmd_args_to_string
from conan.tools.env.environment import Environment
from conan.errors import ConanException

from conan.api.output import (
    ConanOutput,
    LEVEL_QUIET,
    LEVEL_ERROR,
    LEVEL_WARNING,
    LEVEL_STATUS,
    LEVEL_VERBOSE,
    LEVEL_DEBUG,
    LEVEL_TRACE,
)

from conan.internal.util.files import rmdir


def _get_pip_verbosity():
    pass


def _get_uv_verbosity():
    pass


class PyEnv:

    def __init__(self, conanfile, folder=None, name="", py_version=None):
        """
        :param conanfile: The current conanfile ``self``
        :param folder: Optional folder, by default the ``build_folder``
        :param name: Optional name for the virtualenv, by default ``conan_pyenv``
        :param py_version: Optional python version to create the virtualenv using UV
        """
        if sys.version_info.minor < 8 and py_version:
            raise ConanException("'uv' needs Python >= 3.8. Please upgrade your Python interpreter"
                                 " or use 'PyEnv' without defining the 'py_version'.")

        self._conanfile = conanfile
        self._default_python = self._conanfile.conf.get("tools.system.pyenv:python_interpreter")
        # tools.system.pipenv deprecated warning message.
        if not self._default_python and self._conanfile.conf.get("tools.system.pipenv:python_interpreter"):
            self._default_python = self._conanfile.conf.get("tools.system.pipenv:python_interpreter")
            ConanOutput().warning("'tools.system.pipenv:python_interpreter' "
                                  "is deprecated, use 'tools.system.pyenv:python_interpreter'",
                                  warn_tag="deprecated")

        if not self._default_python:
            python = "python" if platform.system() == "Windows" else "python3"
            default_python = shutil.which(python)
            self._default_python = os.path.realpath(default_python) if default_python else None
        if not self._default_python:
            raise ConanException("Conan could not find a Python executable path. Please, install "
                                 "Python system-wide or set the "
                                 "'tools.system.pyenv:python_interpreter' "
                                 "conf to the full path of a Python executable")
        self._env_name = f"conan_pyenv{f'_{name}' if name else ''}"
        if py_version:
            self._env_name += f'_{py_version.replace(".", "_")}'
        base_env_dir = os.path.abspath(folder or conanfile.build_folder)
        self._env_dir = os.path.join(base_env_dir, self._env_name)
        if not os.path.exists(self._env_dir):
            if py_version:
                self._create_uv_venv(base_env_dir, py_version)
            else:
                self._create_venv()

    @property
    def env_dir(self):
        """Root directory of the virtual environment."""
        pass

    @property
    def env_exe(self):
        """Path to the Python executable inside the virtual environment."""
        pass

    @property
    def bin_path(self):
        """Path to the bin or Scripts directory inside the virtual environment."""
        pass

    @staticmethod
    def _get_env_python(env_dir):
        pass

    def generate(self):
        """
        Create a conan environment to use the python venv in the next steps of the conanfile.
        """
        pass

    def run(self, args):
        pass

    def install(self, packages, pip_args=None):
        """
        Will try to install the list of pip packages passed as a parameter.

        :param packages: try to install the list of pip packages passed as a parameter.
        :param pip_args: additional argument list to be passed to the 'pip install' command,
                         e.g.: ['--no-cache-dir', '--index-url', 'https://my.pypi.org/simple'].
                         Defaults to ``None``.
        :return: the return code of the executed pip command.
        """
        pass

    def _create_venv(self):
        pass

    def _create_uv_venv(self, base_env_dir, py_version):
        pass


class PipEnv(PyEnv):
    def __init__(self, conanfile, folder=None, name="", py_version=None):
        super().__init__(conanfile, folder, name, py_version)
        ConanOutput().warning("'PipEnv()' is deprecated, use 'PyEnv()'", warn_tag="deprecated")
