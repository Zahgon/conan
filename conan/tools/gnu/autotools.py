import os
import re

from conan.errors import ConanException
from conan.tools.build import build_jobs, cmd_args_to_string, load_toolchain_args
from conan.internal.subsystems import subsystem_path, deduce_subsystem
from conan.tools.files import chdir
from conan.tools.microsoft import unix_path


def join_arguments(args):
    pass


class Autotools:

    def __init__(self, conanfile, namespace=None):
        """
        :param conanfile: The current recipe object. Always use ``self``.
        :param namespace: this argument avoids collisions when you have multiple toolchain calls in
                          the same recipe. By setting this argument, the *conanbuild.conf* file used
                          to pass information to the toolchain will be named as:
                          *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
                          the name of the generated file is *conanbuild.conf*. This namespace must
                          be also set with the same value in the constructor of the AutotoolsToolchain
                          so that it reads the information from the proper file.
        """
        self._conanfile = conanfile

        toolchain_file_content = load_toolchain_args(self._conanfile.generators_folder,
                                                     namespace=namespace)

        self._configure_args = toolchain_file_content.get("configure_args")
        self._make_args = toolchain_file_content.get("make_args")
        self._autoreconf_args = toolchain_file_content.get("autoreconf_args")

    def configure(self, build_script_folder=None, args=None):
        """
        Call the configure script.

        :param args: List of arguments to use for the ``configure`` call.
        :param build_script_folder: Subfolder where the `configure` script is located. If not specified
                                    conanfile.source_folder is used.
        """
        pass

    def make(self, target=None, args=None, makefile=None):
        """
        Call the make program.

        :param target: (Optional, Defaulted to ``None``): Choose which target to build. This allows
                       building of e.g., docs, shared libraries or install for some AutoTools
                       projects
        :param args: (Optional, Defaulted to ``None``): List of arguments to use for the
                     ``make`` call.
        :param makefile: (Optional, Defaulted to ``None``): Allow specifying a custom makefile to use instead of default "Makefile"
        """
        pass

    def install(self, args=None, target=None, makefile=None):
        """
        This is just an "alias" of ``self.make(target="install")`` or ``self.make(target="install-strip")``

        :param args: (Optional, Defaulted to ``None``): List of arguments to use for the
                     ``make`` call. By default an argument ``DESTDIR=unix_path(self.package_folder)``
                     is added to the call if the passed value is ``None``. See more information about
                     :ref:`tools.microsoft.unix_path() function<conan_tools_microsoft_unix_path>`
        :param target: (Optional, Defaulted to ``None``): Choose which target to install.
        :param makefile: (Optional, Defaulted to ``None``): Allow specifying a custom makefile to use instead of default "Makefile"
        """
        pass

    def autoreconf(self, build_script_folder=None, args=None):
        """
        Call ``autoreconf``

        :param args: (Optional, Defaulted to ``None``): List of arguments to use for the
                     ``autoreconf`` call.
        :param build_script_folder: Subfolder where the `configure` script is located. If not specified
                                    conanfile.source_folder is used.
        """
        pass

    def _use_win_mingw(self):
        pass
