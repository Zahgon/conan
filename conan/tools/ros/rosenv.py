import os
from conan.api.output import Color
from conan.tools.env import Environment
from conan.tools.env.environment import create_env_script


class ROSEnv:
    """
    Generator to serve as integration for Robot Operating System 2 development workspaces.

    IMPORTANT: This generator should be used together with CMakeDeps and CMakeToolchain generators.
    """

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        self.variables = {}
        self._build_script_sh_file = "conanrosenv-build.sh"
        self._build_script_bat_file = "conanrosenv-build.bat"
        self._wrapper_script_sh_file = "conanrosenv.sh"
        self._wrapper_script_bat_file = "conanrosenv.bat"

    def generate(self):
        """
        Creates a ``conanrosenv.sh`` with the environment variables that are needed to build and
        execute ROS packages with Conan dependencies.
        """
        pass

    def _generate_sh_files(self):
        # Generate conanrosenv.sh script wrapper that calls conanbuild.sh and conanrun.sh
        pass

    def _generate_bat_files(self):
        # Generate conanrosenv.bat script wrapper that calls conanbuild.bat and conanrun.bat
        pass
