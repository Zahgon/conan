from pathlib import PurePosixPath, PureWindowsPath, Path
from conan.api.output import Color, ConanOutput
from conan.internal.util.runners import conan_run
from conan.internal.subsystems import subsystem_path
from conan.tools.files import save
from io import StringIO
import tempfile
import os

def wsl_info(msg, error=False):
    pass


class WSLRunner:
    def __init__(self, conan_api, command, host_profile, build_profile, args, raw_args):
        self.conan_api = conan_api
        self.command = command
        self.host_profile = host_profile
        self.build_profile = build_profile
        self.remote_host_profile = None
        self.remote_build_profile = None
        self.remote_python_command = None
        self.remote_conan = None
        self.remote_conan_home = None
        self.args = args
        self.raw_args = raw_args

        # to pass to wsl.exe (optional, otherwise run with defaults)
        distro = host_profile.runner.get("distribution", None)
        user = host_profile.runner.get("user", None)

        self.shared_cache = host_profile.runner.get("shared_cache", False)
        if self.shared_cache:
            storage_path = Path(conan_api.config.home()) / 'p' # TODO: there's an API for this!!
            self.remote_conan_cache = subsystem_path("wsl", storage_path.as_posix())

    def run(self):
        pass
        #print(command)

    def ensure_runner_environment(self):
        pass

    def _copy_profiles(self):
        # TODO: questionable choices, may fail

        # Note: see the use of \\wsl$\<DistroName>\, we could place the files
        #       directly. We would need to work out the exact distro name first
        pass


