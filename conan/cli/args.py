import argparse

from conan.cli.command import OnceArgument
from conan.errors import ConanException

_help_build_policies = '''Optional, specify which packages to build from source. Combining multiple
    '--build' options on one command line is allowed.
    Possible values:

    --build=never      Disallow build for all packages, use binary packages or fail if a binary
                       package is not found, it cannot be combined with other '--build' options.
    --build=missing    Build packages from source whose binary package is not found.
    --build=cascade    Build packages from source that have at least one dependency being built from
                       source.
    --build=[pattern]  Build packages from source whose package reference matches the pattern. The
                       pattern uses 'fnmatch' style wildcards, so '--build="*"' will build everything
                       from source.
    --build=~[pattern] Excluded packages, which will not be built from the source, whose package
                       reference matches the pattern. The pattern uses 'fnmatch' style wildcards.
    --build=missing:[pattern] Build from source if a compatible binary does not exist, only for
                              packages matching pattern.
    --build=compatible:[pattern] (Experimental) Build from source if a compatible binary does not
                                 exist, and the requested package is invalid, the closest package
                                 binary following the defined compatibility policies (method and
                                 compatibility.py)
'''


def add_lockfile_args(parser):
    pass


def add_common_install_arguments(parser):
    pass


def add_profiles_args(parser):
    pass


def add_reference_args(parser):
    pass


def common_graph_args(subparser):
    pass


def validate_common_graph_args(args):
    pass
