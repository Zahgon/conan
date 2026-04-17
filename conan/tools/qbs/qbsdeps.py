from conan.tools.files import save
from conan.errors import ConanException
from conan.internal.model.dependencies import get_transitive_requires
import json
import os


class _QbsDepsModuleFile:
    def __init__(self, qbsdeps, dep, component, deps, module_name):
        self._qbsdeps = qbsdeps
        self._dep = dep
        self._component = component
        self._deps = deps
        self._module_name = module_name
        self._build_bindirs = qbsdeps._build_bindirs
        self._version = (component.get_property("component_version") or
                         component.get_property("system_package_version") or
                         dep.ref.version)

    @property
    def filename(self):
        pass

    @property
    def version(self):
        pass

    def get_content(self):
        pass

    def _get_package_dir(self):
        # If editable, package_folder can be None
        pass

    def render(self):
        return json.dumps(self.get_content(), indent=4)


class _QbsDepGenerator:
    """ Handles a single package, can create multiple modules in case of several components
    """
    def __init__(self, conanfile, dep, build_bindirs):
        self._conanfile = conanfile
        self._dep = dep
        self._build_bindirs = build_bindirs

    @property
    def content(self):
        pass


class QbsDeps:
    """
    This class will generate a JSON file for each dependency inside the "conan-qbs-deps" folder.
    Each JSON file contains information necesary for Qbs ``"conan" module provider`` to be
    able to generate Qbs module files.
    """
    def __init__(self, conanfile):
        """
        :param conanfile: The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile

    @property
    def content(self):
        """
        Returns all dependency information as a Python dict object where key is the dependency
        name and value is a dict with dependency properties.
        """
        pass

    def generate(self):
        """
        This method will save the generated files to the "conan-qbs-deps" directory inside the
        ``conanfile.generators_folder`` directory.
        Generates a single JSON file per dependency or component.
        """
        pass
