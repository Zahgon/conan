from pathlib import Path
import pathlib
import tempfile

from conan.api.output import Color, ConanOutput
from conan.errors import ConanException

import os
from io import BytesIO
import sys

def ssh_info(msg, error=False):
    pass

class SSHRunner:

    def __init__(self, conan_api, command, host_profile, build_profile, args, raw_args):
        try:
            from paramiko.config import SSHConfig
            from paramiko.client import SSHClient
        except ImportError:
            raise ConanException(
                "Paramiko is required for SSH runner. If conan is installed in a virtual environment, try to install "
                "the 'paramiko' package, or consider installing conan package with extra requires 'conan[runners]'"
            )
        self.conan_api = conan_api
        self.command = command
        self.host_profile = host_profile
        self.build_profile = build_profile
        self.remote_host_profile = None
        self.remote_build_profile = None
        self.remote_python_command = None
        self.remote_create_dir = None
        self.remote_is_windows = None
        self.args = args
        self.raw_args = raw_args
        self.ssh_config = None
        self.remote_workspace = None
        self.remote_conan = None
        self.remote_conan_home = None
        if host_profile.runner.get('use_ssh_config', False):
            ssh_config_file = Path.home() / ".ssh" / "config"
            ssh_config = SSHConfig.from_file(open(ssh_config_file))

        hostname = host_profile.runner.get("host") # TODO: this one is required
        if ssh_config and ssh_config.lookup(hostname):
            hostname = ssh_config.lookup(hostname)['hostname']

        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname)


    def run(self, use_cache=True):
        pass

        # self.client.close()
    def ensure_runner_environment(self):
        pass


    def _copy_profiles(self):
        pass

    def copy_working_conanfile_path(self):
        pass

    def _run_command(self, command):
        ''' Run a command in an SSH session.
            When requesting a pseudo-terminal from the server,
            ensure we pass width and height that matches the current
            terminal
        '''
        pass

    def update_local_cache(self, json_result):
        # ('conan list --graph=create.json --graph-binaries=build --format=json > pkglist.json'
        pass
