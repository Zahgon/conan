import os
import subprocess
from pathlib import Path

from conan.api.output import ConanOutput, Color, LEVEL_QUIET
from conan.internal.subsystems import command_env_wrapper
from conan.errors import ConanException
from conan.internal.model.cpp_info import MockInfoProperty
from conan.internal.model.conf import Conf
from conan.internal.model.dependencies import ConanFileDependencies
from conan.internal.model.layout import Folders, Infos, Layouts
from conan.internal.model.options import Options
from conan.internal.model.requires import Requirements
from conan.internal.model.settings import Settings


class ConanFile:
    """
    The base class for all package recipes
    """

    # Reference
    name = None
    version = None  # Any str, can be "1.1" or whatever
    user = None
    channel = None

    # Metadata
    url = None  # The URL where this File is located, as github, to collaborate in package
    license = None
    author = None
    description = None
    topics = None
    homepage = None

    build_policy = None
    upload_policy = None

    exports = None
    exports_sources = None

    generators = []
    revision_mode = "hash"

    # Binary model: Settings and Options
    settings = None
    options = None
    default_options = None
    default_build_options = None
    package_type = None
    vendor = False
    languages = []
    implements = []

    provides = None
    deprecated = None

    win_bash = None
    win_bash_run = None  # For run scope

    _conan_is_consumer = False

    # #### Requirements
    requires = None
    tool_requires = None
    build_requires = None
    test_requires = None
    tested_reference_str = None

    no_copy_source = False
    recipe_folder = None

    # Package information
    cpp = None
    buildenv_info = None
    runenv_info = None
    conf_info = None
    conf = None
    generator_info = None
    conan_data = None

    def __init__(self, display_name=""):
        self.display_name = display_name
        # something that can run commands, as os.sytem

        self._conan_helpers = None
        from conan.tools.env import Environment
        self.buildenv_info = Environment()
        self.runenv_info = Environment()
        # At the moment only for build_requires, others will be ignored
        self.conf_info = Conf()
        self.info = None
        self._conan_buildenv = None  # The profile buildenv, will be assigned initialize()
        self._conan_runenv = None
        self._conan_node = None  # access to container Node object, to access info, context, deps...

        if isinstance(self.generators, str):
            self.generators = [self.generators]
        if isinstance(self.languages, str):
            self.languages = [self.languages]
        if not all(lang == "C" or lang == "C++" for lang in self.languages):
            raise ConanException("Only 'C' and 'C++' languages are allowed in 'languages' attribute")
        if isinstance(self.settings, str):
            self.settings = [self.settings]
        self.requires = Requirements(self.requires, self.build_requires, self.test_requires,
                                     self.tool_requires)

        self.options = Options(self.options or {}, self.default_options)

        if isinstance(self.topics, str):
            self.topics = [self.topics]
        if isinstance(self.provides, str):
            self.provides = [self.provides]

        # user declared variables
        self.user_info = MockInfoProperty("user_info")
        self.env_info = MockInfoProperty("env_info")
        self._conan_dependencies = None

        if not hasattr(self, "virtualbuildenv"):  # Allow the user to override it with True or False
            self.virtualbuildenv = True
        if not hasattr(self, "virtualrunenv"):  # Allow the user to override it with True or False
            self.virtualrunenv = True

        self.env_scripts = {}  # Accumulate the env scripts generated in order
        self.system_requires = {}  # Read only, internal {"apt": []}

        # layout() method related variables:
        self.folders = Folders()
        self.cpp = Infos()
        self.layouts = Layouts()

    def serialize(self):
        pass

    @property
    def output(self):
        # an output stream (writeln, info, warn error)
        pass

    @property
    def context(self):
        pass

    @property
    def subgraph(self):
        pass

    @property
    def dependencies(self):
        # Caching it, this object is requested many times
        pass

    @property
    def ref(self):
        pass

    @property
    def pref(self):
        pass

    @property
    def buildenv(self):
        # Lazy computation of the package buildenv based on the profileone
        pass

    @property
    def runenv(self):
        # Lazy computation of the package runenv based on the profile one
        pass

    @property
    def cpp_info(self):
        """
        Same as using ``self.cpp.package`` in the ``layout()`` method. Use it if you need to read
        the ``package_folder`` to locate the already located artifacts.
        """
        pass

    @cpp_info.setter
    def cpp_info(self, value):
        pass

    @property
    def source_folder(self):
        """
        The folder in which the source code lives. The path is built joining the base directory
        (a cache directory when running in the cache or the ``output folder`` when running locally)
        with the value of ``folders.source`` if declared in the ``layout()`` method.

        :return: A string with the path to the source folder.
        """
        pass

    @property
    def source_path(self) -> Path:
        pass

    @property
    def export_sources_folder(self):
        """
        The value depends on the method you access it:

            - At ``source(self)``: Points to the base source folder (that means self.source_folder but
              without taking into account the ``folders.source`` declared in the ``layout()`` method).
              The declared `exports_sources` are copied to that base source folder always.
            - At ``exports_sources(self)``: Points to the folder in the cache where the export sources
              have to be copied.

        :return: A string with the mentioned path.
        """
        pass

    @property
    def export_sources_path(self) -> Path:
        pass

    @property
    def export_folder(self):
        pass

    @property
    def export_path(self) -> Path:
        pass

    @property
    def build_folder(self):
        """
        The folder used to build the source code. The path is built joining the base directory (a cache
        directory when running in the cache or the ``output folder`` when running locally) with
        the value of ``folders.build`` if declared in the ``layout()`` method.

        :return: A string with the path to the build folder.
        """
        pass

    @property
    def recipe_metadata_folder(self):
        pass

    @property
    def package_metadata_folder(self):
        pass

    @property
    def build_path(self) -> Path:
        pass

    @property
    def package_folder(self):
        """
        The folder to copy the final artifacts for the binary package. In the local cache a package
        folder is created for every different package ID.

        :return: A string with the path to the package folder.
        """
        pass

    @property
    def immutable_package_folder(self):
        pass

    @property
    def generators_folder(self):
        pass

    @property
    def package_path(self) -> Path:
        pass

    @property
    def generators_path(self) -> Path:
        pass

    def run(self, command: str, stdout=None, cwd=None, ignore_errors=False, env="", quiet=False,
            shell=True, scope="build", stderr=None):
        """ Run a command in the current package context.

        :parameter command: The command to run.
        :parameter stdout: The output stream to write the command output. If ``None``, it defaults to
            the standard output stream.
        :parameter stderr: The error output stream to write the command error output. If ``None``,
            it defaults to the standard error stream.
        :parameter cwd: The current working directory to run the command in.
        :parameter ignore_errors: If ``True``, do not raise an error if the command returns a
            non-zero exit code.
        :parameter env: The environment file to use. If empty, it defaults to ``"conanbuild"`` for
            when ``scope`` is ``build`` or ``"conanrun"`` for ``run``.
            If set to ``None`` explicitly, no environment file will be applied,
            which is useful for commands that do not require any environment.
        :parameter quiet: If ``True``, suppress the output of the command.
        :parameter shell: If ``True``, run the command in a shell. This is passed to the
            underlying ``Popen`` function.
        :parameter scope: The scope of the command, either ``"build"`` or ``"run"``.
        """
        pass

    def __repr__(self):
        return self.display_name

    def set_deploy_folder(self, deploy_folder):
        pass
