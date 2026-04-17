import os

import yaml

from conan.internal.cache.home_paths import HomePaths
from conan.internal.default_settings import default_settings_yml
from conan.internal.internal_tools import is_universal_arch
from conan.errors import ConanException
from conan.internal.util.files import save, load


def bad_value_msg(name, value, value_range):
    pass


def undefined_field(name, field, fields=None, value=None):
    pass


class SettingsItem:
    """ represents a setting value and its child info, which could be:
    - A range of valid values: [Debug, Release] (for settings.compiler.runtime of VS)
    - List [None, "ANY"] to accept None or any value
    - A dict {subsetting: definition}, e.g. {version: [], runtime: []} for VS
    """
    def __init__(self, definition, name, value):
        self._definition = definition  # range of possible values
        self._name = name  # settings.compiler
        self._value = value  # gcc

    @staticmethod
    def new(definition, name):
        pass

    def __contains__(self, value):
        return value in (self._value or "")

    def copy(self):
        """ deepcopy, recursive
        """
        pass

    def copy_conaninfo_settings(self):
        """ deepcopy, recursive
        This function adds "ANY" to lists, to allow the ``package_id()`` method to modify some of
        values, but not all, just the "final" values without subsettings.
        We cannot let users manipulate to random strings
        things that contain subsettings like ``compiler``, because that would leave the thing
        in an undefined state, with some now inconsistent subsettings, that cannot be accessed
        anymore. So with this change the options are:
        - If you need more "binary-compatible" descriptions of a compiler, lets say like
        "gcc_or_clang", then you need to add that string to settings.yml. And add the subsettings
        that you want for it.
        - Settings that are "final" (lists), like build_type, or arch or compiler.version they
        can get any value without issues.
        """
        pass

    def __bool__(self):
        if not self._value:
            return False
        return self._value.lower() not in ["false", "none", "0", "off"]

    def __str__(self):
        return str(self._value)

    def __eq__(self, other):
        if other is None:
            return self._value is None
        other = self._validate(other)
        return other == self._value

    def __delattr__(self, item):
        """ This is necessary to remove libcxx subsetting from compiler in config()
           del self.settings.compiler.stdlib
        """
        child_setting = self._get_child(self._value)
        delattr(child_setting, item)

    def _validate(self, value):
        pass

    def _get_child(self, item):
        pass

    def _get_definition(self):
        pass

    def __getattr__(self, item):
        item = str(item)
        sub_config_dict = self._get_child(item)
        return getattr(sub_config_dict, item)

    def __setattr__(self, item, value):
        if item[0] == "_" or item.startswith("value"):
            return super(SettingsItem, self).__setattr__(item, value)

        item = str(item)
        sub_config_dict = self._get_child(item)
        return setattr(sub_config_dict, item, value)

    @property
    def value(self):
        pass

    @value.setter
    def value(self, v):
        pass

    @property
    def values_range(self):
        # This needs to support 2 operations: "in" and iteration. Beware it can return "ANY"
        pass

    @property
    def values_list(self):
        pass

    def validate(self):
        pass

    def possible_values(self):
        pass

    def rm_safe(self, name):
        """ Iterates all possible subsettings, calling rm_safe() for all of them. If removing
        "compiler.cppstd", this will iterate msvc, gcc, clang, etc, calling rm_safe(cppstd) for
        all of them"""
        pass


class Settings:
    def __init__(self, definition=None, name="settings", parent_value="settings"):
        if parent_value is None and definition:
            raise ConanException("settings.yml: null setting can't have subsettings")
        definition = definition or {}
        if not isinstance(definition, dict):
            val = "" if parent_value == "settings" else f"={parent_value}"
            raise ConanException(f"Invalid settings.yml format: '{name}{val}' is not a dictionary")
        self._name = name  # settings, settings.compiler
        self._parent_value = parent_value  # gcc, x86
        self._data = {k: SettingsItem.new(v, f"{name}.{k}") for k, v in definition.items()}
        self._frozen = False

    def serialize(self):
        """
        Returns a dictionary with all the settings (and sub-settings) as ``field: value``
        """
        pass

    def get_safe(self, name, default=None):
        """
        Get the setting value avoiding throwing if it does not exist or has been removed
        :param name:
        :param default:
        :return:
        """
        pass

    def rm_safe(self, name):
        """ Removes the setting or subsetting from the definition. For example,
        rm_safe("compiler.cppstd") remove all "cppstd" subsetting from all compilers, irrespective
        of the current value of the "compiler"
        """
        pass

    def copy(self):
        """ deepcopy, recursive
        """
        pass

    def copy_conaninfo_settings(self):
        pass

    @staticmethod
    def loads(text):
        pass

    def validate(self):
        pass

    @property
    def fields(self):
        pass

    def clear(self):
        pass

    def _check_field(self, field):
        pass

    def __getattr__(self, field):
        assert field[0] != "_", "ERROR %s" % field
        self._check_field(field)
        return self._data[field]

    def __delattr__(self, field):
        assert field[0] != "_", "ERROR %s" % field
        self._check_field(field)
        del self._data[field]

    def __setattr__(self, field, value):
        if field[0] == "_":
            return super(Settings, self).__setattr__(field, value)

        self._check_field(field)
        if self._frozen:
            raise ConanException(f"Tried to define '{field}' setting inside recipe")
        self._data[field].value = value

    @property
    def values_list(self):
        # TODO: make it private, leave .items accessor only
        pass

    def items(self):
        return self.values_list

    def update_values(self, values, raise_undefined=True):
        """
        Receives a list of tuples (compiler.version, value)
        This is more an updater than a setter.
        """
        pass

    def constrained(self, constraint_def):
        """ allows to restrict a given Settings object with the input of another Settings object
        1. The other Settings object MUST be exclusively a subset of the former.
           No additions allowed
        2. If the other defines {"compiler": None} means to keep the full specification
        """
        pass

    def dumps(self):
        """ produces a text string with lines containing a flattened version:
        compiler.arch = XX
        compiler.arch.speed = YY
        """
        pass

    def possible_values(self):
        """Check the range of values of the definition of a setting
        """
        pass


def load_settings_yml(home_folder):
    """Returns {setting: [value, ...]} defining all the possible
               settings without values"""
    pass
