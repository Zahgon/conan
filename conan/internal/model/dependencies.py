from collections import OrderedDict

from conan.api.model import RecipeReference
from conan.errors import ConanException
from conan.internal.graph.graph import RECIPE_PLATFORM
from conan.internal.model.conanfile_interface import ConanFileInterface


class UserRequirementsDict:
    """ user facing dict to allow access of dependencies by name
    """
    def __init__(self, data, require_filter=None):
        self._data = data  # dict-like
        self._require_filter = require_filter  # dict {trait: value} for requirements

    def filter(self, require_filter):
        pass

    def __bool__(self):
        return bool(self._data)

    def get(self, ref, build=None, **kwargs):
        return self._get(ref, build, **kwargs)[1]

    def _get(self, ref, build=None, **kwargs):
        pass

    def __getitem__(self, name):
        return self.get(name)

    def __delitem__(self, name):
        r, _ = self._get(name)
        del self._data[r]

    def items(self):
        return self._data.items()

    def values(self):
        pass

    def __contains__(self, item):
        try:
            self.get(item)
            return True
        except KeyError:
            return False
        except ConanException:
            # ConanException is raised when there are more than one matching the filters
            # so it's definitely in the dict
            return True


class ConanFileDependencies(UserRequirementsDict):

    @staticmethod
    def from_node(node):
        pass

    def filter(self, require_filter, remove_system=True):
        # FIXME: Copy of hte above, to return ConanFileDependencies class object
        pass

    def transitive_requires(self, other):
        """
        :type other: ConanFileDependencies
        """
        pass

    @property
    def topological_sort(self):
        # Return first independent nodes, final ones are the more direct deps
        pass

    @property
    def direct_host(self):
        pass

    @property
    def direct_build(self):
        pass

    @property
    def host(self):
        pass

    @property
    def test(self):
        # Not needed a direct_test because they are visible=False so only the direct consumer
        # will have them in the graph
        pass

    @property
    def build(self):
        pass


def get_transitive_requires(consumer, dependency):
    """ the transitive requires that we need are the consumer ones, not the current dependencey
    ones, so we get the current ones, then look for them in the consumer, and return those
    """
    pass
