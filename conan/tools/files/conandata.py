import os

import yaml

from conan.errors import ConanException
from conan.internal.util.files import load, save


def update_conandata(conanfile, data):
    """
    Tool to modify the ``conandata.yml`` once it is exported. It can be used, for example:

       - To add additional data like the "commit" and "url" for the scm.
       - To modify the contents cleaning the data that belong to other versions (different
         from the exported) to avoid changing the recipe revision when the changed data doesn't
         belong to the current version.

    :param conanfile: The current recipe object. Always use ``self``.
    :param data: (Required) A dictionary (can be nested), of values to update
    """
    pass


def trim_conandata(conanfile, raise_if_missing=True):
    """
    Tool to modify the ``conandata.yml`` once it is exported, to limit it to the current version
    only
    """
    pass
