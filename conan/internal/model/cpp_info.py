import copy
import glob
import json
import os
import re
from collections import OrderedDict, defaultdict

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.model.pkg_type import PackageType
from conan.internal.util.files import load, save

_DIRS_VAR_NAMES = ["_includedirs", "_srcdirs", "_libdirs", "_resdirs", "_bindirs", "_builddirs",
                   "_frameworkdirs", "_objects"]
_FIELD_VAR_NAMES = ["_system_libs", "_package_framework", "_frameworks", "_libs", "_defines",
                    "_cflags", "_cxxflags", "_sharedlinkflags", "_exelinkflags", "_sources"]
_ALL_NAMES = _DIRS_VAR_NAMES + _FIELD_VAR_NAMES
_SINGLE_VALUE_VARS = "_type", "_exe", "_location", "_link_location", "_languages"


class MockInfoProperty:
    """
    # TODO: Remove in 2.X
    to mock user_info and env_info
    """
    counter = {}
    package = None

    def __init__(self, name):
        self._name = name

    @staticmethod
    def message():
        pass

    def __getitem__(self, key):
        MockInfoProperty.counter.setdefault(self._name, set()).add(self.package)
        return []

    def __setitem__(self, key, value):
        MockInfoProperty.counter.setdefault(self._name, set()).add(self.package)

    def __getattr__(self, attr):
        MockInfoProperty.counter.setdefault(self._name, set()).add(self.package)
        return []

    def __setattr__(self, attr, value):
        if attr != "_name":
            MockInfoProperty.counter.setdefault(self._name, set()).add(self.package)
        return super(MockInfoProperty, self).__setattr__(attr, value)


class _Component:

    def __init__(self, set_defaults=False):
        # ###### PROPERTIES
        self._properties = None

        # ###### DIRECTORIES
        self._includedirs = None  # Ordered list of include paths
        self._srcdirs = None  # Ordered list of source paths
        self._libdirs = None  # Directories to find libraries
        self._resdirs = None  # Directories to find resources, data, etc
        self._bindirs = None  # Directories to find executables and shared libs
        self._builddirs = None
        self._frameworkdirs = None

        # ##### FIELDS
        self._system_libs = None  # Ordered list of system libraries
        self._frameworks = None  # system Apple OS frameworks
        self._package_framework = None  # any other frameworks
        self._libs = None  # The libs to link against
        self._defines = None  # preprocessor definitions
        self._cflags = None  # pure C flags
        self._cxxflags = None  # C++ compilation flags
        self._sharedlinkflags = None  # linker flags
        self._exelinkflags = None  # linker flags
        self._objects = None  # linker flags
        self._sources = None  # source files
        self._exe = None  # application executable, only 1 allowed, following CPS
        self._languages = None

        self._sysroot = None
        self._requires = None

        # LEGACY 1.X fields, can be removed in 2.X
        self.names = MockInfoProperty("cpp_info.names")
        self.filenames = MockInfoProperty("cpp_info.filenames")
        self.build_modules = MockInfoProperty("cpp_info.build_modules")

        if set_defaults:
            self.includedirs = ["include"]
            self.libdirs = ["lib"]
            self.bindirs = ["bin"]

        # CPS
        self._type = None
        self._location = None
        self._link_location = None

    def serialize(self):
        pass

    @staticmethod
    def deserialize(contents):
        pass

    def clone(self):
        # Necessary below for exploding a cpp_info.libs = [lib1, lib2] into components
        pass

    @property
    def includedirs(self):
        pass

    @includedirs.setter
    def includedirs(self, value):
        pass

    @property
    def srcdirs(self):
        pass

    @srcdirs.setter
    def srcdirs(self, value):
        pass

    @property
    def libdirs(self):
        pass

    @libdirs.setter
    def libdirs(self, value):
        pass

    @property
    def resdirs(self):
        pass

    @resdirs.setter
    def resdirs(self, value):
        pass

    @property
    def bindirs(self):
        pass

    @bindirs.setter
    def bindirs(self, value):
        pass

    @property
    def builddirs(self):
        pass

    @builddirs.setter
    def builddirs(self, value):
        pass

    @property
    def bindir(self):
        pass

    @property
    def libdir(self):
        pass

    @property
    def includedir(self):
        pass

    @property
    def system_libs(self):
        pass

    @system_libs.setter
    def system_libs(self, value):
        pass

    @property
    def package_framework(self):
        pass

    @package_framework.setter
    def package_framework(self, value):
        pass

    @property
    def frameworks(self):
        pass

    @frameworks.setter
    def frameworks(self, value):
        pass

    @property
    def frameworkdirs(self):
        pass

    @frameworkdirs.setter
    def frameworkdirs(self, value):
        pass

    @property
    def libs(self):
        pass

    @libs.setter
    def libs(self, value):
        pass

    @property
    def exe(self):
        pass

    @exe.setter
    def exe(self, value):
        pass

    @property
    def type(self):
        pass

    @type.setter
    def type(self, value):
        pass

    @property
    def location(self):
        pass

    @location.setter
    def location(self, value):
        pass

    @property
    def link_location(self):
        pass

    @link_location.setter
    def link_location(self, value):
        pass

    @property
    def languages(self):
        pass

    @languages.setter
    def languages(self, value):
        pass

    @property
    def defines(self):
        pass

    @defines.setter
    def defines(self, value):
        pass

    @property
    def cflags(self):
        pass

    @cflags.setter
    def cflags(self, value):
        pass

    @property
    def cxxflags(self):
        pass

    @cxxflags.setter
    def cxxflags(self, value):
        pass

    @property
    def sharedlinkflags(self):
        pass

    @sharedlinkflags.setter
    def sharedlinkflags(self, value):
        pass

    @property
    def exelinkflags(self):
        pass

    @exelinkflags.setter
    def exelinkflags(self, value):
        pass

    @property
    def objects(self):
        pass

    @objects.setter
    def objects(self, value):
        pass

    @property
    def sources(self):
        pass

    @sources.setter
    def sources(self, value):
        pass

    @property
    def sysroot(self):
        pass

    @sysroot.setter
    def sysroot(self, value):
        pass

    @property
    def requires(self):
        pass

    @requires.setter
    def requires(self, value):
        pass

    @property
    def required_component_names(self):
        """ Names of the required INTERNAL components of the same package (not scoped with ::)"""
        pass

    def set_property(self, property_name, value):
        pass

    def get_property(self, property_name, check_type=None):
        pass

    def get_init(self, attribute, default):
        # Similar to dict.setdefault
        pass

    def merge(self, other, overwrite=False):
        """
        @param overwrite:
        @type other: _Component
        """
        pass

    def set_relative_base_folder(self, folder):
        pass

    def deploy_base_folder(self, package_folder, deploy_folder):
        pass

    def parsed_requires(self):
        pass

    def _auto_deduce_locations(self, conanfile, library_name):

        pass

    def deduce_locations(self, conanfile, component_name=""):
        pass


class CppInfo:

    def __init__(self, set_defaults=False):
        self.components = defaultdict(lambda: _Component(set_defaults))
        self.default_components = None
        self._package = _Component(set_defaults)

    def __getattr__(self, attr):
        # all cpp_info.xxx of not defined things will go to the global package
        return getattr(self._package, attr)

    def __setattr__(self, attr, value):
        if attr in ("components", "default_components", "_package", "_aggregated", "required_components"):
            super(CppInfo, self).__setattr__(attr, value)
        else:
            setattr(self._package, attr, value)

    def serialize(self):
        pass

    def deserialize(self, content):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass

    @property
    def has_components(self):
        pass

    def merge(self, other, overwrite=False):
        """Merge 'other' into self. 'other' can be an old cpp_info object
        Used to merge Layout source + build cpp objects info (editables)
        @type other: CppInfo
        @param other: The other CppInfo to merge
        @param overwrite: New values from other overwrite the existing ones
        """
        pass

    def set_relative_base_folder(self, folder):
        """Prepend the folder to all the directories definitions, that are relative"""
        pass

    def deploy_base_folder(self, package_folder, deploy_folder):
        """Prepend the folder to all the directories"""
        pass

    def get_sorted_components(self):
        """
        Order the components taking into account if they depend on another component in the
        same package (not scoped with ::). First less dependant.

        :return: ``OrderedDict`` {component_name: component}
        """
        pass

    def aggregated_components(self):
        """Aggregates all the components as global values, returning a new CppInfo
        Used by many generators to obtain a unified, aggregated view of all components
        """
        pass

    def check_component_requires(self, conanfile):
        """ quality check for component requires, called by BinaryInstaller after package_info()
        - Check that all recipe ``requires`` are used if consumer recipe explicit opt-in to use
          component requires
        - Check that component external dep::comp dependency "dep" is a recipe "requires"
        - Check that every internal component require actually exist
        It doesn't check that external components do exist
        """
        pass

    @property
    def required_components(self):
        """Returns a list of tuples with (require, component_name) required by the package
        If the require is internal (to another component), the require will be None"""
        pass

    def deduce_full_cpp_info(self, conanfile):
        pass
