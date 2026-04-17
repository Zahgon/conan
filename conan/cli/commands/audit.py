import json
import os

from conan.api.conan_api import ConanAPI
from conan.api.input import UserInput
from conan.api.model import MultiPackagesList, RecipeReference
from conan.api.output import cli_out_write, ConanOutput
from conan.api.subapi.audit import CONAN_CENTER_AUDIT_PROVIDER_NAME
from conan.cli import make_abs_path
from conan.cli.args import common_graph_args, validate_common_graph_args
from conan.cli.command import conan_command, conan_subcommand
from conan.cli.formatters.audit.vulnerabilities import text_vuln_formatter, json_vuln_formatter, \
    html_vuln_formatter
from conan.cli.printers import print_profiles
from conan.cli.printers.graph import print_graph_basic
from conan.errors import ConanException


def _add_provider_arg(subparser):
    pass


def _parse_error_threshold(result: dict, error_level: float) -> None:
    """Mark the result as error if any of the vulnerabilities has a severity greater than or equal to
       The error_level reflects the severity level configured by the user. As it uses float and CVSS
       score is limited to 10.0, users can use any higher number to skip it.

       :param result: Conan audit scan result. It's expected to find cvss there
       :param error_level: Threshold to raise an error in case of matching the severity level
       :return: None
    """
    pass


@conan_subcommand(formatters={"text": text_vuln_formatter,
                              "json": json_vuln_formatter,
                              "html": html_vuln_formatter})
def audit_scan(conan_api: ConanAPI, parser, subparser, *args) -> dict:
    """
    Scan a given recipe for vulnerabilities in its dependencies.
    """
    pass


@conan_subcommand(formatters={"text": text_vuln_formatter,
                              "json": json_vuln_formatter,
                              "html": html_vuln_formatter})
def audit_list(conan_api: ConanAPI, parser, subparser, *args):
    """
    List the vulnerabilities of the given reference.
    """
    pass


def _text_provider_formatter(providers_action):
    pass


def _json_provider_formatter(providers_action):
    pass


@conan_subcommand(formatters={"text": _text_provider_formatter, "json": _json_provider_formatter})
def audit_provider(conan_api, parser, subparser, *args):
    """
    Manage security providers for the 'conan audit' command.
    """
    pass


@conan_command(group="Security")
def audit(conan_api, parser, *args):  # noqa
    """
    Find vulnerabilities in your dependencies.
    """
