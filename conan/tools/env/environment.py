import os
import textwrap
from shlex import quote
from collections import OrderedDict
from contextlib import contextmanager

from conan.api.output import ConanOutput
from conan.internal.subsystems import deduce_subsystem, WINDOWS, subsystem_path
from conan.errors import ConanException
from conan.internal.model.recipe_ref import ref_matches
from conan.internal.util.files import save


class _EnvVarPlaceHolder:
    pass


def environment_wrap_command(conanfile, env_filenames, env_folder, cmd, subsystem=None,
                             accepted_extensions=None):
    pass


class _EnvValue:
    def __init__(self, name, value=None, separator=" ", path=False):
        self._name = name
        self._values = [] if value is None else value if isinstance(value, list) else [value]
        self._path = path
        self._sep = separator

    def __bool__(self):
        return bool(self._values)  # Empty means unset

    def dumps(self):
        pass

    def copy(self):
        pass

    @property
    def is_path(self):
        pass

    def remove(self, value):
        pass

    def append(self, value, separator=None):
        pass

    def prepend(self, value, separator=None):
        pass

    def compose_env_value(self, other):
        """
        :type other: _EnvValue
        """
        pass

    def get_str(self, placeholder, subsystem, pathsep, root_path=None, script_path=None):
        """
        :param subsystem:
        :param placeholder: a OS dependant string pattern of the previous env-var value like
        $PATH, %PATH%, et
        :param pathsep: The path separator, typically ; or :
        :param root_path: To do a relativize of paths, the base root path to be replaced
        :param script_path: the replacement instead of the script path
        :return: a string representation of the env-var value, including the $NAME-like placeholder
        """
        pass

    def get_value(self, subsystem, pathsep):
        pass

    def deploy_base_folder(self, package_folder, deploy_folder):
        """Make the path relative to the deploy_folder"""
        pass

    def set_relative_base_folder(self, folder):
        pass


class Environment:
    """
    Generic class that helps to define modifications to the environment variables.
    """

    def __init__(self):
        # It being ordered allows for Windows case-insensitive composition
        self._values = OrderedDict()  # {var_name: [] of values, including separators}

    def __bool__(self):
        return bool(self._values)

    def copy(self):
        pass

    def __repr__(self):
        return repr(self._values)

    def dumps(self):

        """
        :return: A string with a profile-like original definition, not the full environment
                 values
        """
        pass

    def define(self, name, value, separator=" "):
        """
        Define `name` environment variable with value `value`

        :param name: Name of the variable
        :param value: Value that the environment variable will take
        :param separator: The character to separate appended or prepended values
        """
        pass

    def define_path(self, name, value):
        pass

    def unset(self, name):
        """
        clears the variable, equivalent to a unset or set XXX=

        :param name: Name of the variable to unset
        """
        pass

    def append(self, name, value, separator=None):
        """
        Append the `value` to an environment variable `name`

        :param name: Name of the variable to append a new value
        :param value: New value
        :param separator: The character to separate the appended value with the previous value. By default it will use a blank space.
        """
        pass

    def append_path(self, name, value):
        """
        Similar to "append" method but indicating that the variable is a filesystem path. It will automatically handle the path separators depending on the operating system.

        :param name: Name of the variable to append a new value
        :param value: New value
        """
        pass

    def prepend(self, name, value, separator=None):
        """
        Prepend the `value` to an environment variable `name`

        :param name: Name of the variable to prepend a new value
        :param value: New value
        :param separator: The character to separate the prepended value with the previous value
        """
        pass

    def prepend_path(self, name, value):
        """
        Similar to "prepend" method but indicating that the variable is a filesystem path. It will automatically handle the path separators depending on the operating system.

        :param name: Name of the variable to prepend a new value
        :param value: New value
        """
        pass

    def remove(self, name, value):
        """
        Removes the `value` from the variable `name`.

        :param name: Name of the variable
        :param value: Value to be removed.
        """
        pass

    def compose_env(self, other):
        """
        Compose an Environment object with another one.
        ``self`` has precedence, the "other" will add/append if possible and not
        conflicting, but ``self`` mandates what to do. If ``self`` has ``define()``, without
        placeholder, that will remain.

        :param other: the "other" Environment
        :type other: class:`Environment`
        """
        pass

    def __eq__(self, other):
        """
        :param other: the "other" environment
        :type other: class:`Environment`
        """
        return other._values == self._values

    def vars(self, conanfile, scope="build"):
        """
        :param conanfile: Instance of a conanfile, usually ``self`` in a recipe
        :param scope: Determine the scope of the declared variables.
        :return: An EnvVars object from the current Environment object
        """
        pass

    def deploy_base_folder(self, package_folder, deploy_folder):
        """Make the paths relative to the deploy_folder"""
        pass

    def set_relative_base_folder(self, folder):
        pass


class EnvVars:
    """
    Represents an instance of environment variables for a given system. It is obtained from the generic Environment class.

    """
    def __init__(self, conanfile, values, scope):
        self._values = values  # {var_name: _EnvValue}, just a reference to the Environment
        self._conanfile = conanfile
        self._scope = scope
        self._subsystem = deduce_subsystem(conanfile, scope)
        self._deactivation_mode = conanfile.conf.get("tools.env:deactivation_mode", default=None, check_type=str)

    @property
    def _pathsep(self):
        pass

    def __getitem__(self, name):
        return self._values[name].get_value(self._subsystem, self._pathsep)

    def keys(self):
        pass

    def get(self, name, default=None, variable_reference=None):
        """ get the value of a env-var

        :param name: The name of the environment variable.
        :param default: The returned value if the variable doesn't exist, by default None.
        :param variable_reference: if specified, use a variable reference instead of the
                                   pre-existing value of environment variable, where {name}
                                   can be used to refer to the name of the variable.
        """
        v = self._values.get(name)
        if v is None:
            return default
        if variable_reference:
            return v.get_str(variable_reference, self._subsystem, self._pathsep)
        else:
            return v.get_value(self._subsystem, self._pathsep)

    def items(self, variable_reference=None):
        """returns {str: str} (varname: value)

        :param variable_reference: if specified, use a variable reference instead of the
                                   pre-existing value of environment variable, where {name}
                                   can be used to refer to the name of the variable.
        """
        if variable_reference:
            return {k: v.get_str(variable_reference, self._subsystem, self._pathsep)
                    for k, v in self._values.items()}.items()
        else:
            return {k: v.get_value(self._subsystem, self._pathsep)
                    for k, v in self._values.items()}.items()

    @contextmanager
    def apply(self):
        """
        Context manager to apply the declared variables to the current ``os.environ`` restoring
        the original environment when the context ends.

        """
        pass

    def save_dotenv(self, file_location):
        pass

    def save_bat(self, file_location, generate_deactivate=True):
        pass

    def save_ps1(self, file_location, generate_deactivate=True):
        pass

    def save_sh(self, file_location, generate_deactivate=True):
        pass

    def save_script(self, filename):
        """
        Saves a script file (bat, sh, ps1) with a launcher to set the environment.
        If the conf "tools.env.virtualenv:powershell" is not an empty string
        it will generate powershell
        launchers if Windows.

        :param filename: Name of the file to generate. If the extension is provided, it will generate
                         the launcher script for that extension, otherwise the format will be deduced
                         checking if we are running inside Windows (checking also the subsystem) or not.
        """
        pass


def _deactivate_func_name(filename):
    pass


def _old_env_prefix(filename):
    pass


def _ps1_deactivate_contents(deactivation_mode, values, filename):
    pass


def _sh_deactivate_contents(deactivation_mode, values, filename):
    pass


class ProfileEnvironment:
    def __init__(self):
        self._environments = OrderedDict()

    def __repr__(self):
        return repr(self._environments)

    def __bool__(self):
        return bool(self._environments)

    def get_profile_env(self, ref, is_consumer=False):
        """ computes package-specific Environment
        it is only called when conanfile.buildenv is called
        the last one found in the profile file has top priority
        """
        pass

    def update_profile_env(self, other):
        """
        :type other: ProfileEnvironment
        :param other: The argument profile has priority/precedence over the current one.
        """
        pass

    def dumps(self):
        pass

    @staticmethod
    def loads(text):
        pass


def create_env_script(conanfile, content, filename, scope="build"):
    """
    Create a file with any content which will be registered as a new script for the defined "scope".

    Args:
        conanfile: The Conanfile instance.
        content (str): The content of the script to write into the file.
        filename (str): The name of the file to be created in the generators folder.
        scope (str): The scope or environment group for which the script will be registered.
    """
    pass


def register_env_script(conanfile, env_script_path, scope="build"):
    """
    Add the "env_script_path" to the current list of registered scripts for defined "scope"
    These will be mapped to files:
    - conan{group}.bat|sh = calls env_script_path1,... env_script_pathN

    Args:
        conanfile: The Conanfile instance.
        env_script_path (str): The full path of the script to register.
        scope (str): The scope ('build' or 'host') for which the script will be registered.
    """
    pass


def generate_aggregated_env(conanfile):

    pass


def _relativize_paths(conanfile, placeholder):
    pass
