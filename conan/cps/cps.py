import json
import os
from enum import Enum

from conan.internal.model.cpp_info import CppInfo
from conan.internal.util.files import save, load


class CPSComponentType(Enum):
    DYLIB = "dylib"
    ARCHIVE = "archive"
    INTERFACE = "interface"
    EXE = "executable"
    JAR = "jar"
    UNKNOWN = "unknown"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        # This is useful for comparing with string type at user code, like ``type == "xxx"``
        return super().__eq__(CPSComponentType(other))

    @staticmethod
    def from_conan(pkg_type):
        pass


class CPSComponent:
    def __init__(self, component_type=None):
        self.includes = []
        self.type = component_type or "unknown"
        self.definitions = {}
        self.requires = []
        self.link_requires = []
        self.location = None
        self.link_location = None
        self.link_languages = []
        self.link_libraries = []  # system libraries

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data):
        pass

    @staticmethod
    def from_cpp_info(cpp_info, conanfile, libname=None):
        pass

    def update(self, conf, conf_def):
        # TODO: conf not used at the moent
        self.link_languages = self.link_languages or conf_def.get("link_languages")
        self.location = self.location or conf_def.get("location")
        self.link_location = self.link_location or conf_def.get("link_location")
        self.link_libraries = self.link_libraries or conf_def.get("link_libraries")


class CPS:
    """ represents the CPS file for 1 package
    """
    def __init__(self, name=None, version=None):
        self.name = name
        self.version = version
        self.default_components = []
        self.components = {}
        self.configurations = []
        self.requires = []
        # Supplemental
        self.description = None
        self.license = None
        self.website = None
        self.prefix = None

    def serialize(self):
        pass

    @staticmethod
    def deserialize(data):
        pass

    @staticmethod
    def from_conan(dep):
        pass

    def to_conan(self):
        pass

    def save(self, folder):
        pass

    @staticmethod
    def load(file):
        pass
