from conan.errors import ConanException


def _get_gnu_arch(os_, arch):
    # Calculate the arch
    pass


def _get_gnu_os(os_, arch, compiler=None):
    # Calculate the OS
    pass


def _get_gnu_triplet(os_, arch, compiler=None):
    """
    Returns string with <machine>-<vendor>-<op_system> triplet (<vendor> can be omitted in practice)

    :param os_: os to be used to create the triplet
    :param arch: arch to be used to create the triplet
    :param compiler: compiler used to create the triplet (only needed fo windows)
    """
    pass
