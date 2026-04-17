from conan.api.output import ConanOutput, Color, LEVEL_VERBOSE, LEVEL_DEBUG


def print_graph_basic(graph):
    # I am excluding the "download"-"cache" or remote information, that is not
    # the definition of the graph, but some history how it was computed
    # maybe we want to summarize that info after the "GraphBuilder" ends?
    # TODO: Should all of this be printed from a json representation of the graph? (the same json
    #   that would be in the json_formatter for the graph?)
    pass


def print_graph_packages(graph):
    # I am excluding the "download"-"cache" or remote information, that is not
    # the definition of the graph, but some history how it was computed
    # maybe we want to summarize that info after the "GraphBuilder" ends?
    pass
