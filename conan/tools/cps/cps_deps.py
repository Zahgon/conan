from conan.cps.cps import CPS
from conan.tools.files import save

import json
import os


class CPSDeps:
    def __init__(self, conanfile):
        self._conanfile = conanfile

    def _config_name(self):
        pass

    def generate(self):
        pass
