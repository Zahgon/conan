from argparse import Namespace
import os
import sys
import json
import platform
import shutil
from typing import Optional, NamedTuple, Dict, List
import yaml
from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern
from conan.api.output import Color, ConanOutput
from conan.cli import make_abs_path
from conan.internal.runner import RunnerException
from conan.errors import ConanException
from pathlib import Path
from conan.internal.model.profile import Profile
from conan.internal.model.version import Version
from conan.internal.runner.output import RunnerOutput


class _ContainerConfig(NamedTuple):
    class Build(NamedTuple):
        dockerfile: Optional[str] = None
        build_context: Optional[str] = None
        build_args: Optional[Dict[str, str]] = None
        cache_from: Optional[List[str]] = None
        platform: Optional[str] = None

    class Run(NamedTuple):
        name: Optional[str] = None
        environment: Optional[Dict[str, str]] = None
        user: Optional[str] = None
        privileged: Optional[bool] = None
        cap_add: Optional[List[str]] = None
        security_opt: Optional[List[str]] = None
        volumes: Optional[Dict[str, str]] = None
        network: Optional[str] = None

    image: Optional[str] = None
    build: Build = Build()
    run: Run = Run()

    @staticmethod
    def load(file_path: Optional[str]) -> '_ContainerConfig':
        # Container config
        # https://containers.dev/implementors/json_reference/
        pass


class DockerRunner:
    def __init__(self, conan_api: ConanAPI, command: str, host_profile: Profile, build_profile: Profile, args: Namespace, raw_args: list[str]):
        self.logger = ConanOutput()
        self.docker_client = self._initialize_docker_client()
        self.docker_api = self.docker_client.api
        self.conan_api = conan_api
        self.build_profile = build_profile
        self.abs_host_path = self._get_abs_host_path(args.path)
        self.args = args
        if args.format:
            raise ConanException("format argument is forbidden if running in a docker runner")

        self.configfile = _ContainerConfig.load(host_profile.runner.get('configfile'))
        self.dockerfile = host_profile.runner.get('dockerfile') or self.configfile.build.dockerfile
        self.docker_build_context = host_profile.runner.get('build_context') or self.configfile.build.build_context
        self.platform = host_profile.runner.get('platform') or self.configfile.build.platform
        self.image = host_profile.runner.get('image') or self.configfile.image
        if not (self.dockerfile or self.image):
            raise ConanException("'dockerfile' or docker image name is needed")
        self.image = self.image or 'conan-runner-default'
        self.name = self.configfile.run.name or host_profile.runner.get("name", "conan-runner-docker")
        self.remove = str(host_profile.runner.get('remove', 'false')).lower() == 'true'
        self.cache = str(host_profile.runner.get('cache', 'clean'))
        if self.cache not in ['clean', 'copy', 'shared']:
            raise ConanException(f'Invalid cache value: "{self.cache}". Valid values are: clean, copy, shared')
        self.container = None
        self.raw_args = raw_args
        self.command = command
        self.runner_logger = RunnerOutput(self.name)

    def run(self) -> None:
        """
        Run conan inside a Docker container
        """
        pass

    def _initialize_docker_client(self):
        pass

    def _get_abs_host_path(self, path: str) -> Path:
        pass

    def _build_image(self) -> None:
        pass

    def _start_container(self) -> None:
        pass

    def _run_command(self, command: str, workdir: Optional[str] = None, verbose: bool = True) -> tuple[str, str]:
        pass

    def _get_volumes_and_docker_path(self) -> tuple[dict, str]:
        pass

    def _create_runner_environment(self) -> tuple[dict, dict]:
        # Runner configuration
        pass

    def _init_container(self) -> None:
        pass

    def _update_local_cache(self) -> None:
        pass
