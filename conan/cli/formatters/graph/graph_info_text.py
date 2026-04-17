import fnmatch

from conan.api.model import RecipeReference
from conan.api.output import ConanOutput, cli_out_write


def filter_graph(graph, package_filter=None, field_filter=None):
    pass


def format_graph_info(result):
    """ More complete graph output, including information for every node in the graph
    Used for 'graph info' command
    """
    pass


def _serial_pretty_printer(data, indent=""):
    pass
