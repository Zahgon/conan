
def cross_building(conanfile=None, skip_x64_x86=False):
    """
    Check if we are cross building comparing the *build* and *host* settings. Returns ``True``
    in the case that we are cross-building.

    :param conanfile: The current recipe object. Always use ``self``.
    :param skip_x64_x86: Do not consider cross building when building to 32 bits from 64 bits:
           x86_64 to x86, sparcv9 to sparc or ppc64 to ppc32
    :return: ``bool`` value from ``tools.build.cross_building:cross_build`` if exists, otherwise,
             it returns ``True`` if we are cross-building, else, ``False``.
    """
    pass


def can_run(conanfile):
    """
    Validates whether is possible to run a non-native app on the same architecture.
    It’s a useful feature for the case your architecture can run more than one target.
    For instance, Mac M1 machines can run both `armv8` and `x86_64`.

    :param conanfile: The current recipe object. Always use ``self``.
    :return: ``bool`` value from ``tools.build.cross_building:can_run`` if exists, otherwise,
             it returns ``False`` if we are cross-building, else, ``True``.
    """
    pass
