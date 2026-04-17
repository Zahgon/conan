import itertools
import glob
import re

from conan.internal import check_duplicated_generator
from conan.internal.util.files import save
from conan.tools.premake.constants import CONAN_TO_PREMAKE_ARCH

# Filename format strings
PREMAKE_VAR_FILE = "conan_{pkgname}_vars_{config}.premake5.lua"
PREMAKE_PKG_FILE = "conan_{pkgname}.premake5.lua"
PREMAKE_ROOT_FILE = "conandeps.premake5.lua"

PREMAKE_CONFIG_FILE = "conanconfig_{config}.premake5.lua"
PREMAKE_CONFIG_ROOT_FILE = "conanconfig.premake5.lua"

# File template format strings
PREMAKE_TEMPLATE_CONFIG = """
include "conanutils.premake5.lua"

t_conan_deps_order = {{}}
t_conan_deps_order["{config}"] = {{{order}}}

if conan_deps_order == nil then conan_deps_order = {{}} end
conan_premake_tmerge(conan_deps_order, t_conan_deps_order)
"""
PREMAKE_TEMPLATE_UTILS = """
function conan_premake_tmerge(dst, src)
    for k, v in pairs(src) do
        if type(v) == "table" then
            if type(dst[k] or 0) == "table" then
                conan_premake_tmerge(dst[k] or {}, src[k] or {})
            else
                dst[k] = v
            end
        else
            dst[k] = v
        end
    end
    return dst
end
"""
PREMAKE_TEMPLATE_VAR = """
include "conanutils.premake5.lua"

t_conandeps = {{}}
t_conandeps["{config}"] = {{}}
t_conandeps["{config}"]["{pkgname}"] = {{}}
t_conandeps["{config}"]["{pkgname}"]["includedirs"] = {{{deps.includedirs}}}
t_conandeps["{config}"]["{pkgname}"]["libdirs"] = {{{deps.libdirs}}}
t_conandeps["{config}"]["{pkgname}"]["bindirs"] = {{{deps.bindirs}}}
t_conandeps["{config}"]["{pkgname}"]["libs"] = {{{deps.libs}}}
t_conandeps["{config}"]["{pkgname}"]["system_libs"] = {{{deps.system_libs}}}
t_conandeps["{config}"]["{pkgname}"]["defines"] = {{{deps.defines}}}
t_conandeps["{config}"]["{pkgname}"]["cxxflags"] = {{{deps.cxxflags}}}
t_conandeps["{config}"]["{pkgname}"]["cflags"] = {{{deps.cflags}}}
t_conandeps["{config}"]["{pkgname}"]["sharedlinkflags"] = {{{deps.sharedlinkflags}}}
t_conandeps["{config}"]["{pkgname}"]["exelinkflags"] = {{{deps.exelinkflags}}}
t_conandeps["{config}"]["{pkgname}"]["frameworks"] = {{{deps.frameworks}}}

if conandeps == nil then conandeps = {{}} end
conan_premake_tmerge(conandeps, t_conandeps)
"""
PREMAKE_TEMPLATE_ROOT_BUILD = """
        includedirs(conandeps[conf][pkg]["includedirs"])
        bindirs(conandeps[conf][pkg]["bindirs"])
        defines(conandeps[conf][pkg]["defines"])
"""
PREMAKE_TEMPLATE_ROOT_LINK = """
        libdirs(conandeps[conf][pkg]["libdirs"])
        links(conandeps[conf][pkg]["libs"])
        links(conandeps[conf][pkg]["system_libs"])
        links(conandeps[conf][pkg]["frameworks"])
"""
PREMAKE_TEMPLATE_ROOT_FUNCTION = """
function {function_name}(conf, pkg)
    if conf == nil then
{filter_call}
    elseif pkg == nil then
        local order = conan_deps_order[conf]
        for index, lib in ipairs(order) do
            {function_name}(conf, lib)
        end
    else
{lua_content}
    end
end
"""
PREMAKE_TEMPLATE_ROOT_GLOBAL = """
function conan_setup(conf, pkg)
    conan_setup_build(conf, pkg)
    conan_setup_link(conf, pkg)
end
"""


# Helper class that expands cpp_info meta information in lua readable string sequences
class _PremakeTemplate:
    def __init__(self, req, dep_cpp_info):
        def _format_paths(paths):
            pass

        def _format_flags(flags):
            pass

        # Headers dependant
        with_headers = req and req.headers
        self.includedirs = _format_paths(dep_cpp_info.includedirs if with_headers else [])
        self.defines = _format_flags(dep_cpp_info.defines if with_headers else [])
        self.cxxflags = _format_flags(dep_cpp_info.cxxflags if with_headers else [])
        self.cflags = _format_flags(dep_cpp_info.cflags if with_headers else [])
        self.sharedlinkflags = _format_flags(dep_cpp_info.sharedlinkflags if with_headers else [])
        self.exelinkflags = _format_flags(dep_cpp_info.exelinkflags if with_headers else [])

        # Libs dependant
        with_libs = req and req.libs
        self.libs = _format_flags(dep_cpp_info.libs if with_libs else [])
        self.libdirs = _format_paths(dep_cpp_info.libdirs if with_libs else [])

        # Run dependant
        with_run = req and req.run
        self.bindirs = _format_paths(dep_cpp_info.bindirs if with_run else [])

        self.system_libs = _format_flags(dep_cpp_info.system_libs)
        self.frameworks = ", ".join('"%s.framework"' % p.replace('"', '\\"') for p in
                                    dep_cpp_info.frameworks) if dep_cpp_info.frameworks else ""
        self.sysroot = f"{dep_cpp_info.sysroot}".replace("\\", "/") \
            if dep_cpp_info.sysroot else ""


class PremakeDeps:
    """
    PremakeDeps class generator
    conandeps.premake5.lua: unconditional import of all *direct* dependencies only
    """

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """

        self._conanfile = conanfile

        # Tab configuration
        self.tab = "    "

        # Return value buffer
        self.output_files = {}
        # Extract configuration and architecture form conanfile
        self.configuration = conanfile.settings.build_type
        self.architecture = conanfile.settings.arch

    def generate(self):
        """
        Generates ``conan_<pkg>_vars_<config>.premake5.lua``, ``conan_<pkg>_<config>.premake5.lua``,
        and ``conan_<pkg>.premake5.lua`` files into the ``conanfile.generators_folder``.
        """
        pass

    def _config_suffix(self):
        pass

    def _output_lua_file(self, filename, content):
        pass

    def _indent_string(self, string, indent=1):
        pass

    def _premake_filtered(self, content, configuration, architecture, indent=0):
        """
        - Surrounds the lua line(s) contained within ``content`` with a premake "filter" and returns the result.
        - A "filter" will affect all premake function calls after it's set. It's used to limit following project
          setup function call(s) to a certain scope. Here it is used to limit the calls in content to only apply
          if the premake ``configuration`` and ``architecture`` matches the parameters in this function call.
        """
        pass

    @property
    def content(self):
        pass
