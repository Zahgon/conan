import json
import os

from jinja2 import Template, select_autoescape

from conan.api.output import cli_out_write
from conan.cli.formatters.graph.graph_info_text import filter_graph
from conan.cli.formatters.graph.info_graph_dot import graph_info_dot
from conan.cli.formatters.graph.info_graph_html import graph_info_html


def _render_graph(graph, template, template_folder):
    pass


def format_graph_html(result):
    pass


def format_graph_dot(result):
    pass


def format_graph_json(result):
    pass
