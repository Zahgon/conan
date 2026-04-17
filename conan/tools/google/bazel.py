import os
import platform

from conan.tools.google import BazelToolchain


class Bazel:

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile
        # Use BazelToolchain generated file if exists
        self._conan_bazelrc = os.path.join(self._conanfile.generators_folder, BazelToolchain.bazelrc_name)
        self._use_conan_config = os.path.exists(self._conan_bazelrc)
        self._startup_opts = self._get_startup_command_options()

    def _safe_run_command(self, command):
        """
        Windows is having problems stopping bazel processes, so it ends up locking
        some files if something goes wrong. Better to shut down the Bazel server after running
        each command.
        """
        pass

    def _get_startup_command_options(self):
        pass

    def build(self, args=None, target="//...", clean=True):
        """
        Runs "bazel <rcpaths> build <configs> <args> <targets>" command where:

        * ``rcpaths``: adds ``--bazelrc=xxxx`` per rc-file path. It listens to ``BazelToolchain``
          (``--bazelrc=conan_bzl.rc``), and ``tools.google.bazel:bazelrc_path`` conf.
        * ``configs``: adds ``--config=xxxx`` per bazel-build configuration.
          It listens to ``BazelToolchain`` (``--config=conan-config``), and
          ``tools.google.bazel:configs`` conf.
        * ``args``: they are any extra arguments to add to the ``bazel build`` execution.
        * ``targets``: all the target labels.

        :param target: It is the target label. By default, it's "//..." which runs all the targets.
        :param args: list of extra arguments to pass to the CLI.
        :param clean: boolean that indicates to run a "bazel clean" before running the "bazel build".
                      Notice that this is important to ensure a fresh bazel cache every
        """
        pass

    def test(self, target=None):
        """
        Runs "bazel test <targets>" command.
        """
        pass
