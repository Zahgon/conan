import copy
from collections import OrderedDict, defaultdict

from conan.errors import ConanException
from conan.tools.env.environment import ProfileEnvironment
from conan.internal.model.conf import ConfDefinition
from conan.internal.model.options import Options
from conan.api.model import RecipeReference


class Profile:
    """A profile contains a set of setting (with values), environment variables
    """

    def __init__(self):
        # Input sections, as defined by user profile files and command line
        self.settings = OrderedDict()
        self.package_settings = defaultdict(OrderedDict)
        self.options = Options()
        self.tool_requires = OrderedDict()  # ref pattern: list of ref
        self.replace_requires = {}
        self.replace_tool_requires = {}
        self.platform_tool_requires = []
        self.platform_requires = []
        self.conf = ConfDefinition()
        self.buildenv = ProfileEnvironment()
        self.runenv = ProfileEnvironment()
        self.runner = {}

        # Cached processed values
        self.processed_settings = None  # Settings with values, and smart completion
        self._package_settings_values = None

    def __repr__(self):
        return self.dumps()

    def serialize(self):
        pass

    @property
    def package_settings_values(self):
        pass

    def process_settings(self, cache_settings):
        pass

    def dumps(self):
        pass

    def compose_profile(self, other):
        pass

    def update_settings(self, new_settings):
        """Mix the specified settings with the current profile.
        Specified settings are prioritized to profile"""
        pass

    def update_package_settings(self, package_settings):
        """Mix the specified package settings with the specified profile.
        Specified package settings are prioritized to profile"""
        pass
