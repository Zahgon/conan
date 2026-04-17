import os

from conan.api.output import ConanOutput
from conan.cli.command import conan_command, OnceArgument, conan_subcommand

from conan.cli import make_abs_path
from conan.cli.args import common_graph_args, validate_common_graph_args
from conan.cli.printers.graph import print_graph_packages, print_graph_basic
from conan.errors import ConanException
from conan.api.model import RecipeReference


@conan_command(group="Consumer")
def lock(conan_api, parser, *args):  # noqa
    """
    Create or manage lockfiles.
    """


@conan_subcommand()
def lock_create(conan_api, parser, subparser, *args):
    """
    Create a lockfile from a conanfile or a reference.
    """
    pass


@conan_subcommand()
def lock_merge(conan_api, parser, subparser, *args): # noqa
    """
    Merge 2 or more lockfiles.
    """
    pass


@conan_subcommand()
def lock_add(conan_api, parser, subparser, *args):
    """
    Add requires, build-requires or python-requires to an existing or new lockfile.
    The resulting lockfile will be ordered, newer versions/revisions first.
    References can be supplied with and without revisions like "--requires=pkg/version",
    but they must be recipe references, including at least the version,
    and they cannot contain a version range.
    """
    pass


@conan_subcommand()
def lock_remove(conan_api, parser, subparser, *args):
    """
    Remove requires, build-requires or python-requires from an existing lockfile.
    References can be supplied with and without revisions like "--requires=pkg/version",
    """
    pass


@conan_subcommand()
def lock_update(conan_api, parser, subparser, *args):
    """
    Update requires, build-requires or python-requires from an existing lockfile.
    References that matches the arguments package names will be replaced by the arguments.
    References can be supplied with and without revisions like "--requires=pkg/version",
    """
    pass


@conan_subcommand()
def lock_upgrade(conan_api, parser, subparser, *args):
    """
    (Experimental) Upgrade requires, build-requires or python-requires from an existing lockfile
    given a conanfile or a reference.
    """
    pass


@conan_subcommand()
def lock_upgrade_config(conan_api, parser, subparser, *args):
    """
    (Experimental) Upgrade config requires in a lockfile
    """
    pass
