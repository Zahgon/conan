import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from io import StringIO

from conan.errors import ConanException
from conan.internal.util.files import load


if getattr(sys, 'frozen', False) and 'LD_LIBRARY_PATH' in os.environ:

    # http://pyinstaller.readthedocs.io/en/stable/runtime-information.html#ld-library-path-libpath-considerations
    pyinstaller_bundle_dir = os.environ['LD_LIBRARY_PATH'].replace(
        os.environ.get('LD_LIBRARY_PATH_ORIG', ''), ''
    ).strip(';:')

    @contextmanager
    def pyinstaller_bundle_env_cleaned():
        """Removes the pyinstaller bundle directory from LD_LIBRARY_PATH
        """
        pass

else:
    @contextmanager
    def pyinstaller_bundle_env_cleaned():
        pass


def conan_run(command, stdout=None, stderr=None, cwd=None, shell=True):
    """
    @param shell:
    @param stderr:
    @param command: Command to execute
    @param stdout: Instead of print to sys.stdout print to that stream. Could be None
    @param cwd: Move to directory to execute
    """
    pass


def detect_runner(command):
    # Running detect.py automatic detection of profile
    pass


def check_output_runner(cmd, stderr=None, ignore_error=False):
    # Used to run several utilities, like Pacman detect, AIX version, uname, SCM
    pass
