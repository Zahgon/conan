import os
import shutil
import platform
import textwrap

from jinja2 import Template
from conan.internal import check_duplicated_generator
from conan.errors import ConanException
from conan.tools.env import VirtualBuildEnv
from conan.tools.microsoft import msvs_toolset
from conan.tools.microsoft.visual import vs_installation_path, _vcvars_path, _vcvars_versions
from conan.tools.qbs import common
from conan.internal.util.files import save


def _find_msvc(conanfile):
    pass


def _find_clangcl(conanfile):
    pass


class _LinkerFlagsParser:
    def __init__(self, ld_flags):
        self.driver_linker_flags = []
        self.linker_flags = []

        for item in ld_flags:
            if item.startswith('-Wl'):
                self.linker_flags.extend(item.split(',')[1:])
            else:
                self.driver_linker_flags.append(item)


class QbsProfile:
    """
    Qbs profiles generator.

    This class generates file with the toolchain information that can be imported by Qbs.
    """

    def __init__(self, conanfile, profile='conan', default_profile='conan'):
        """
        :param conanfile: The current recipe object. Always use ``self``.
        :param profile: The name of the profile in settings. Defaults to ``"conan"``.
        :param default_profile: The name of the default profile. Defaults to ``"conan"``.

        """
        self._conanfile = conanfile
        self._profile = profile
        self._default_profile = default_profile

        self.extra_cflags = []
        self.extra_cxxflags = []
        self.extra_defines = []
        self.extra_sharedlinkflags = []
        self.extra_exelinkflags = []

        self._build_env = VirtualBuildEnv(self._conanfile, auto_generate=True).vars()

    @property
    def filename(self):
        """
        The name of the generated file. Returns ``qbs_settings.txt``.
        """
        pass

    @property
    def content(self):
        """
        Returns the content of the settings file as dict of Qbs properties.
        """
        pass

    def render(self):
        """
        Returns the content of the settings file as string.
        """
        template = textwrap.dedent('''\
            {%- for key, value in profile_values.items() %}
            profiles.{{profile}}.{{ key }}:{{ value }}
            {%- endfor %}
            defaultProfile: {{default_profile}}
        ''')
        t = Template(template)
        context = {
            'profile_values': self.content,
            'profile': self._profile,
            'default_profile': self._default_profile,
        }
        result = t.render(**context)
        return result

    def generate(self):
        """
        This method will save the generated files to the conanfile.generators_folder.

        Generates the "qbs_settings.txt" file. This file contains Qbs settings such as toolchain
        properties and can be imported using ``qbs config --import``.
        """
        pass

    def _check_for_compiler(self):
        pass

    def _get_qbs_toolchain(self):
        pass

    def _default_compiler_names(self, toolchain):
        pass

    def _find_exe(self, exe):
        pass

    def _toolchain_properties(self):
        pass

    def _properties_from_settings(self):
        pass

    def _properties_from_options(self):
        pass

    def _properties_from_conf(self):
        pass
