import json
import os

from jinja2 import Template, select_autoescape

from conan.api.output import cli_out_write
from conan.cli.formatters.list.search_table_html import list_packages_html_template
from conan import __version__


def list_packages_html(result):
    pass
