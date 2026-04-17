import os
import shutil

from conan.tools.build import build_jobs, cmd_args_to_string
from conan.errors import ConanException

def _configuration_dict_to_commandlist(name, config_dict):
    pass


class Qbs:
    """
    Qbs helper to use together with the QbsDeps feature.
    This class provides helper methods that wraps calls to the Qbs tool.
    """
    def __init__(self, conanfile, project_file=None):
        """
        :param conanfile: The current recipe object. Always use ``self``.
        :param project_file: The name to the main project file. If not set, Qbs will try to
            autodetect the project file.
        """
        self.profile = None
        self._conanfile = conanfile
        self._set_project_file(project_file)
        self.jobs = build_jobs(conanfile)
        self._configuration = dict()

    def _set_project_file(self, project_file):
        pass

    def add_configuration(self, name, values):
        """
        Adds a build configuration for the multi-configuration build.
        This Qbs feature is rarely needed since each conan package can contain only one
        configuration, however might be useful when creating multiple versions of the same product
        that should be put in the same Conan package.

        :param name: the name of the configuration. This corresponds to the ``config`` parameter
            of ``qbs resolve``, ``qbs build`` and ``qbs install`` commands.
        :param values: the dict containing Qbs properties and their values for this configuration.
        """
        pass

    def _qbs_settings_paths(self):
        pass

    def _get_common_arguments(self):
        pass

    def resolve(self, parallel=True):
        """
        Wraps the ``qbs resolve`` call.
        If QbsDeps generator is used, this will also set the necessary properites of the Qbs
        "conan" module provider automatically adding dependencies to the project.
        :param parallel: Whether to use multi-threaded resolving. Defaults to ``True``.
        """
        pass

    def _build(self, products, all_products):

        pass

    def build(self, products=None):
        """
        Wraps the ``qbs build`` call.

        :param products: The list of product names to build. If not set, builds all products that
            have builtByDefault set to true. This parameter corresponds to the ``--products``
            option of the ``qbs build`` command.

        The resolve() method should be called before calling this method.
        """
        pass

    def build_all(self):
        """
        Wraps the ``qbs build --all-products`` call.
        This method builds all products, even if their builtByDefault property is false.
        The resolve() method should be called before calling this method.
        """
        pass

    def install(self):
        """
        Wraps the ``qbs install`` call.
        Perfoms the installation of files marked as installable in the Qbs project.
        The build() or build_all() methods should be called before calling this method.
        """
        pass
