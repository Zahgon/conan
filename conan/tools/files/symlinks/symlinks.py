import os


def get_symlinks(base_folder):
    """Return the absolute path to the symlink files in base_folder"""
    pass


def _path_inside(base, folder):
    pass


def absolute_to_relative_symlinks(conanfile, base_folder):
    """
    Convert the symlinks with absolute paths into relative ones if they are pointing to a file or
    directory inside the ``base_folder``. Any absolute symlink pointing outside the ``base_folder``    will be ignored.

    :param conanfile: The current recipe object. Always use ``self``.
    :param base_folder: Folder to be scanned.
    """
    pass


def remove_external_symlinks(conanfile, base_folder):
    """
    Remove the symlinks to files that point outside the ``base_folder``, no matter if relative or absolute.

    :param conanfile: The current recipe object. Always use ``self``.
    :param base_folder: Folder to be scanned.
    """
    pass


def remove_broken_symlinks(conanfile, base_folder=None):
    """
    Remove the broken symlinks, no matter if relative or absolute.

    :param conanfile: The current recipe object. Always use ``self``.
    :param base_folder: Folder to be scanned.
    """
    pass
