
import fnmatch
import re
from functools import total_ordering

from conan.errors import ConanException
from conan.internal.model.version import Version
from conan.internal.util.dates import timestamp_to_str


@total_ordering
class RecipeReference:
    """ An exact (no version-range, no alias) reference of a recipe,
    it represents a reference of the form ``name/version[@user/channel][#revision][%timestamp]``.
    Should be enough to locate a recipe in the cache or in a server, and
    validation will be external to this class, at specific points (export, api, etc).
    """

    def __init__(self, name=None, version=None, user=None, channel=None, revision=None,
                 timestamp=None):
        """ The attributes should be regarded as immutable, and should not be modified by the user."""
        #: Name of the reference
        self.name: str = name
        if version is not None and not isinstance(version, Version):
            version = Version(version)
        #: Version of the reference
        self.version: Version = version  # This MUST be a version if we want to be able to order
        #: User of the reference, if any
        self.user = user
        #: Channel of the reference, if any
        self.channel = channel
        #: Revision of the reference, if any
        self.revision = revision
        #: Timestamp of the reference, if any
        self.timestamp = timestamp

    def copy(self):
        # Used for creating copy in lockfile-overrides mechanism
        pass

    def __repr__(self):
        """ long repr like pkg/0.1@user/channel#rrev%timestamp """
        result = self.repr_notime()
        if self.timestamp is not None:
            result += "%{}".format(self.timestamp)
        return result

    def repr_notime(self):
        pass

    def repr_humantime(self):
        pass

    def __str__(self):
        """ shorter representation, excluding the revision and timestamp """
        if self.name is None:
            return ""
        result = "/".join([self.name, str(self.version)])
        if self.user:
            result += "@{}".format(self.user)
        if self.channel:
            assert self.user
            result += "/{}".format(self.channel)
        return result

    def __lt__(self, ref):
        # The timestamp goes before the revision for ordering revisions chronologically
        # In theory this is enough for sorting
        # When no timestamp is given, it will always have lower priority, to avoid comparison
        # errors float <> None
        return (self.name, self.version, self.user or "", self.channel or "", self.timestamp or 0,
                self.revision or "") \
               < (ref.name, ref.version, ref.user or "", ref.channel or "", ref.timestamp or 0,
                  ref.revision or "")

    def __eq__(self, ref):
        # Timestamp doesn't affect equality.
        # This is necessary for building an ordered list of UNIQUE recipe_references for Lockfile
        if ref is None:
            return False
        # If one revision is not defined, they are equal
        if self.revision is not None and ref.revision is not None:
            return (self.name, self.version, self.user, self.channel, self.revision) == \
                   (ref.name, ref.version, ref.user, ref.channel, ref.revision)
        return (self.name, self.version, self.user, self.channel) == \
               (ref.name, ref.version, ref.user, ref.channel)

    def __hash__(self):
        # This is necessary for building an ordered list of UNIQUE recipe_references for Lockfile
        return hash((self.name, self.version, self.user, self.channel))

    @staticmethod
    def loads(rref):
        """ Instantiates an object from a string, in the form:
        ``name/version[@user/channel][#revision][%timestamp]``"""
        pass

    def validate_ref(self, allow_uppercase=False):
        """ Check that the reference is valid, and raise a ``ConanException`` if not.
        """
        pass

    def matches(self, pattern, is_consumer):
        """ fnmatches the reference against the provided pattern.

        :parameter str pattern: the pattern to match against, it can contain wildcards,
            and can start with ``!`` or ``~`` to negate the match.
            A special value of ``&`` will return a match only of ``is_consumer`` is ``True``
        :parameter bool is_consumer: if ``True``, the pattern ``&`` will match this reference.
        """
        pass

    def partial_match(self, pattern):
        # Finds if pattern matches any of partial sums of tokens of conan reference
        pass


class PkgReference:

    def __init__(self, ref=None, package_id=None, revision=None, timestamp=None):
        self.ref = ref
        self.package_id = package_id
        self.revision = revision
        self.timestamp = timestamp  # float, Unix seconds UTC

    def __repr__(self):
        """ long repr like pkg/0.1@user/channel#rrev%timestamp """
        if self.ref is None:
            return ""
        result = repr(self.ref)
        if self.package_id:
            result += ":{}".format(self.package_id)
        if self.revision is not None:
            result += "#{}".format(self.revision)
        if self.timestamp is not None:
            result += "%{}".format(self.timestamp)
        return result

    def repr_notime(self):
        pass

    def repr_humantime(self):
        pass

    def __str__(self):
        """ shorter representation, excluding the revision and timestamp """
        if self.ref is None:
            return ""
        result = str(self.ref)
        if self.package_id:
            result += ":{}".format(self.package_id)
        return result

    def __lt__(self, ref):
        # The timestamp goes before the revision for ordering revisions chronologically
        raise Exception("WHO IS COMPARING PACKAGE REFERENCES?")
        # return (self.name, self.version, self.user, self.channel, self.timestamp, self.revision) \
        #       < (ref.name, ref.version, ref.user, ref.channel, ref._timestamp, ref.revision)

    def __eq__(self, other):
        # TODO: In case of equality, should it use the revision and timestamp?
        # Used:
        #    at "graph_binaries" to check: cache_latest_prev != pref
        #    at "installer" to check: if pkg_layout.reference != pref (probably just optimization?)
        #    at "revisions_test"
        return self.ref == other.ref and self.package_id == other.package_id and \
               self.revision == other.revision

    def __hash__(self):
        # Used in dicts of PkgReferences as keys like the cached nodes in the graph binaries
        return hash((self.ref, self.package_id, self.revision))

    @staticmethod
    def loads(pkg_ref):  # TODO: change this default to validate only on end points
        pass
