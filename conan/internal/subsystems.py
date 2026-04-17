"""
Potential scenarios:

- Running from a Windows native "cmd"
  - Targeting Windows native (os.subsystem = None)
    - No need of bash (no conf at all)
    - Need to build in bash (tools.microsoft.bash:subsystem=xxx,
                             tools.microsoft.bash:path=<path>,
                             conanfile.win_bash)
    - Need to run (tests) in bash (tools.microsoft.bash:subsystem=xxx,
                                   tools.microsoft.bash:path=<path>,
                                   conanfile.win_bash_run)
  - Targeting Subsystem (os.subsystem = msys2/cygwin)
    - Always builds and runs in bash (tools.microsoft.bash:path)

- Running from a subsytem terminal (tools.microsoft.bash:subsystem=xxx,
                                    tools.microsoft.bash:path=None) NO ERROR mode for not specifying it? =CURRENT?
  - Targeting Windows native (os.subsystem = None)
  - Targeting Subsystem (os.subsystem = msys2/cygwin)

"""
import os
import platform
import re

from conan.tools.build import cmd_args_to_string
from conan.errors import ConanException

WINDOWS = "windows"
MSYS2 = 'msys2'
MSYS = 'msys'
CYGWIN = 'cygwin'
WSL = 'wsl'  # Windows Subsystem for Linux


def command_env_wrapper(conanfile, command, envfiles, envfiles_folder, scope="build"):
    pass


def _windows_bash_wrapper(conanfile, command, env, envfiles_folder):
    pass


def _escape_windows_cmd(command):
    """ To use in a regular windows cmd.exe
        1. Adds escapes so the argument can be unpacked by CommandLineToArgvW()
        2. Adds escapes for cmd.exe so the argument survives cmd.exe's substitutions.

        Useful to escape commands to be executed in a windows bash (msys2, cygwin etc)
    """
    pass


def deduce_subsystem(conanfile, scope):
    """ used by:
    - EnvVars: to decide if using :  ; as path separator, translate paths to subsystem
               and decide to generate a .bat or .sh
    - Autotools: to define the full abs path to the "configure" script
    - GnuDeps: to map all the paths from dependencies
    - Aggregation of envfiles: to map each aggregated path to the subsystem
    - unix_path: util for recipes
    """
    pass


def subsystem_path(subsystem, path):
    """"Used to translate windows paths to MSYS unix paths like
    c/users/path/to/file. Not working in a regular console or MinGW!
    """
    pass


def get_cased_path(name):
    pass
