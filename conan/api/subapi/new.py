import fnmatch
import os
import shutil

from jinja2 import Template, StrictUndefined, UndefinedError, Environment, meta

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.util.files import load, save
from conan import __version__


class NewAPI:
    _NOT_TEMPLATES = "not_templates"  # Filename containing filenames of files not to be rendered

    def __init__(self, conan_api):
        self._conan_api = conan_api

    def save_template(self, template, defines=None, output_folder=None, force=False):
        """
        Save the 'template' files in the output_folder, replacing the template variables
        with the 'defines'
        :param template: The name of the template to use
        :param defines: A list with the 'k=v' variables to replace in the template
        :param output_folder: The folder where the template files will be saved, cwd if None
        :param force: If True, overwrite the files if they already exist, otherwise raise an error
        """
        pass

    @staticmethod
    def get_builtin_template(template_name):
        pass

    def get_template(self, template_folder):
        """ Load a template from a user absolute folder
        """
        pass

    def get_home_template(self, template_name):
        """ Load a template from the Conan home templates/command/new folder
        """
        pass

    def _read_files(self, template_folder):
        pass

    @staticmethod
    def render(template_files, definitions):
        result = {}
        name = definitions.get("name", "mypkg")
        if isinstance(name, list):
            raise ConanException(f"name argument can't be multiple: {name}")
        if name != name.lower():
            raise ConanException(f"name argument must be lowercase: {name}")
        definitions["conan_version"] = __version__

        def ensure_list(key):
            pass

        ensure_list("requires")
        ensure_list("tool_requires")

        def as_package_name(n):
            pass

        def as_name(ref):
            pass

        definitions["package_name"] = as_package_name(name).replace(".", "_")
        definitions["as_name"] = as_name
        definitions["names"] = lambda x: ", ".join(r.split("/", 1)[0] for r in x)
        if "name" not in definitions:
            definitions["name"] = "mypkg"
        if "version" not in definitions:
            definitions["version"] = "0.1"
        version = definitions.get("version")
        if isinstance(version, list):
            raise ConanException(f"version argument can't be multiple: {version}")

        try:
            for k, v in template_files.items():
                k = Template(k, keep_trailing_newline=True, undefined=StrictUndefined).render(
                    **definitions)
                v = Template(v, keep_trailing_newline=True, undefined=StrictUndefined).render(
                    **definitions)
                if v:
                    result[k] = v
        except UndefinedError:
            template_vars = []
            for templ_str in template_files.values():
                env = Environment()
                ast = env.parse(templ_str)
                template_vars.extend(meta.find_undeclared_variables(ast))

            injected_vars = {"conan_version", "package_name", "as_name"}
            optional_vars = {"requires", "tool_requires", "output_root_dir"}
            template_vars = list(set(template_vars) - injected_vars - optional_vars)
            template_vars.sort()

            raise ConanException("Missing definitions for the template. "
                                 "Required definitions are: {}"
                                 .format(", ".join("'{}'".format(var) for var in template_vars)))
        return result
