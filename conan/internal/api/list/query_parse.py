from collections import OrderedDict


def filter_package_configs(pkg_configurations, query):
    pass


def _evaluate_postfix_with_info(postfix, binary_info):

    # Evaluate conaninfo with the expression

    pass


def _evaluate(prop_name, prop_value, binary_info):
    """
    Evaluates a single prop_name, prop_value like "os", "Windows" against
    conan_vars_info.serialize_min()
    """
    pass


def _is_operator(el):
    pass


def _parse_expression(subexp):
    """Expressions like:
     compiler.version=12
     compiler="Visual Studio"
     arch="x86"
     Could be replaced with another one to parse different queries """
    pass


def _evaluate_postfix(postfix, evaluator):
    """
    Evaluates a postfix expression and returns a boolean
    @param postfix:  Postfix expression as a list
    @param evaluator: Function that will return a bool receiving expressions
                      like "compiler.version=12"
    @return: bool
    """
    pass


def _infix_to_postfix(exp):
    """
    Translates an infix expression to postfix using an standard algorithm
    with little hacks for parse complex expressions like "compiler.version=4"
    instead of just numbers and without taking in account the operands priority
    except the priority specified by the "("

    @param exp: String with an expression with & and | operators,
        e.g.: "os=Windows & (compiler=gcc | compiler.version=3)"
        e.g.: "os=Windows AND (compiler=gcc or compiler.version=3)"
    @return List with the postfix expression
    """
    pass
