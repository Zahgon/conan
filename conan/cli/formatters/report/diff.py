import json
import os
import base64

from jinja2 import Template

from conan.api.output import cli_out_write
from conan.cli.formatters.report.diff_html import diff_html


def _generate_json(result):
    pass


def _get_filenames(line, src_prefix, dst_prefix):
    """
    Extracts the source and destination filenames from a diff line.
    """
    pass


def _render_diff(content, template, template_folder, **kwargs):
    pass


def format_diff_html(result):
    pass


def format_diff_txt(result):
    pass


def format_diff_json(result):
    pass
