from conan.errors import ConanException
from conan.internal.model.pkg_type import PackageType
from conan.api.model import RecipeReference
from conan.internal.model.version_range import VersionRange


class Requirement:
    """ A user definition of a requires in a conanfile
    """
    def __init__(self, ref, *, headers=None, libs=None, build=False, run=None, visible=None,
                 transitive_headers=None, transitive_libs=None, test=None, package_id_mode=None,
                 force=None, override=None, direct=None, options=None, no_skip=False):
        # * prevents the usage of more positional parameters, always ref + **kwargs
        # By default this is a generic library requirement
        self.ref = ref
        self._required_ref = ref  # Store the original reference
        self._headers = headers  # This dependent node has headers that must be -I<headers-path>
        self._libs = libs
        self._build = build  # This dependent node is a build tool that runs at build time only
        self._run = run  # node contains executables, shared libs or data necessary at host run time
        self._visible = visible  # Even if not libsed or visible, the node is unique, can conflict
        self._transitive_headers = transitive_headers
        self._transitive_libs = transitive_libs
        self._test = test
        self._package_id_mode = package_id_mode
        self._force = force
        self._override = override
        self._direct = direct
        self.options = options
        # Meta and auxiliary information
        # The "defining_require" is the require that defines the current value. If this require is
        # overriden/forced, this attribute will point to the overriding/forcing requirement.
        self.defining_require = self  # if not overriden, it points to itself
        self.overriden_ref = None  # to store if the requirement has been overriden (store old ref)
        self.override_ref = None  # to store if the requirement has been overriden (store new ref)
        self.is_test = test  # to store that it was a test, even if used as regular requires too
        self.skip = False
        self.required_nodes = set()  # store which intermediate nodes are required, to compute "Skip"
        self.no_skip = no_skip

    @property
    def files(self):  # require needs some files in dependency package
        pass

    @staticmethod
    def _default_if_none(field, default_value):
        pass

    @property
    def headers(self):
        pass

    @headers.setter
    def headers(self, value):
        pass

    @property
    def libs(self):
        pass

    @libs.setter
    def libs(self, value):
        pass

    @property
    def visible(self):
        pass

    @visible.setter
    def visible(self, value):
        pass

    @property
    def test(self):
        pass

    @test.setter
    def test(self, value):
        pass

    @property
    def force(self):
        pass

    @force.setter
    def force(self, value):
        pass

    @property
    def override(self):
        pass

    @override.setter
    def override(self, value):
        pass

    @property
    def direct(self):
        pass

    @direct.setter
    def direct(self, value):
        pass

    @property
    def build(self):
        pass

    @build.setter
    def build(self, value):
        pass

    @property
    def run(self):
        pass

    @run.setter
    def run(self, value):
        pass

    @property
    def transitive_headers(self):
        pass

    @transitive_headers.setter
    def transitive_headers(self, value):
        pass

    @property
    def transitive_libs(self):
        pass

    @transitive_libs.setter
    def transitive_libs(self, value):
        pass

    @property
    def package_id_mode(self):
        pass

    @package_id_mode.setter
    def package_id_mode(self, value):
        pass

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        traits = 'build={}, headers={}, libs={}, '  \
                 'run={}, visible={}'.format(self.build, self.headers, self.libs, self.run,
                                             self.visible)
        return "{}, Traits: {}".format(self.ref, traits)

    def serialize(self):
        pass

    def copy_requirement(self):
        pass

    @property
    def version_range(self):
        """ returns the version range expression, without brackets []
        or None if it is not an expression
        """
        pass

    @property
    def alias(self):
        pass

    def process_package_type(self, src_node, node):
        """If the requirement traits have not been adjusted, then complete them with package type
        definition"""
        pass

    def __hash__(self):
        return hash((self.ref.name, self.build))

    def __eq__(self, other):
        """If the name is the same and they are in the same context, and if both of them are
        propagating includes or libs or run info or both are visible or the reference is the same,
        we consider the requires equal, so they can conflict"""
        return (self.ref.name == other.ref.name and self.build == other.build and
                (self.override or  # an override with same name and context, always match
                 (self.headers and other.headers) or
                 (self.libs and other.libs) or
                 (self.run and other.run) or
                 ((self.visible or self.test) and (other.visible or other.test)) or
                 (self.ref == other.ref and self.options == other.options)))

    def aggregate(self, other):
        """ when closing loop and finding the same dependency on a node, the information needs
        to be aggregated
        :param other: is the existing Require that the current node has, which information has to be
        appended to "self", which is the requires that is being propagated to the current node
        from upstream
        """
        pass

    def transform_downstream(self, pkg_type, require, dep_pkg_type):
        """
        consumer ---self--->  foo<pkg_type> ---require---> bar<dep_pkg_type>
            \\ -------------------????-------------------- /
        Compute new Requirement to be applied to "consumer" translating the effect of the dependency
        to such "consumer".
        Result can be None if nothing is to be propagated
        """
        pass

    def deduce_package_id_mode(self, pkg_type, dep_node, non_embed_mode, embed_mode, build_mode,
                               unknown_mode):
        # If defined by the ``require(package_id_mode=xxx)`` trait, that is higher priority
        # The "conf" values are defaults, no hard overrides
        pass

        # For cases like Application->Application, without headers or libs, package_id_mode=None
        # It will be independent by default


class BuildRequirements:
    # Just a wrapper around requires for backwards compatibility with self.build_requires() syntax
    def __init__(self, requires):
        self._requires = requires

    def __call__(self, ref, package_id_mode=None, visible=False, run=None, options=None,
                 override=None):
        # TODO: Check which arguments could be user-defined
        self._requires.build_require(ref, package_id_mode=package_id_mode, visible=visible, run=run,
                                     options=options, override=override)


class ToolRequirements:
    # Just a wrapper around requires for backwards compatibility with self.build_requires() syntax
    def __init__(self, requires):
        self._requires = requires

    def __call__(self, ref, package_id_mode=None, visible=False, run=True, options=None,
                 override=None):
        # TODO: Check which arguments could be user-defined
        self._requires.tool_require(ref, package_id_mode=package_id_mode, visible=visible, run=run,
                                    options=options, override=override)


class TestRequirements:
    # Just a wrapper around requires for backwards compatibility with self.build_requires() syntax
    def __init__(self, requires):
        self._requires = requires

    def __call__(self, ref, run=None, options=None, force=None):
        self._requires.test_require(ref, run=run, options=options, force=force)


class Requirements:
    """ User definitions of all requires in a conanfile
    """
    def __init__(self, declared=None, declared_build=None, declared_test=None,
                 declared_build_tool=None):
        self._requires = {}
        # Construct from the class definitions
        if declared is not None:
            if isinstance(declared, str):
                self.__call__(declared)
            else:
                try:
                    for item in declared:
                        if not isinstance(item, str):
                            # TODO (2.X): Remove protection after transition from 1.X
                            raise ConanException(f"Incompatible 1.X requires declaration '{item}'")
                        self.__call__(item)
                except TypeError:
                    raise ConanException("Wrong 'requires' definition, "
                                         "did you mean 'requirements()'?")
        if declared_build is not None:
            if isinstance(declared_build, str):
                self.build_require(declared_build)
            else:
                try:
                    for item in declared_build:
                        self.build_require(item)
                except TypeError:
                    raise ConanException("Wrong 'build_requires' definition, "
                                         "did you mean 'build_requirements()'?")
        if declared_test is not None:
            if isinstance(declared_test, str):
                self.test_require(declared_test)
            else:
                try:
                    for item in declared_test:
                        self.test_require(item)
                except TypeError:
                    raise ConanException("Wrong 'test_requires' definition, "
                                         "did you mean 'build_requirements()'?")
        if declared_build_tool is not None:
            if isinstance(declared_build_tool, str):
                self.build_require(declared_build_tool, run=True)
            else:
                try:
                    for item in declared_build_tool:
                        self.build_require(item, run=True)
                except TypeError:
                    raise ConanException("Wrong 'tool_requires' definition, "
                                         "did you mean 'build_requirements()'?")

    def reindex(self, require, new_name):
        """ This operation is necessary when the reference name of a package is changed
        as a result of an "alternative" replacement of the package name, otherwise the dictionary
        gets broken by modified key
        """
        pass

    def values(self):
        pass

    # TODO: Plan the interface for smooth transition from 1.X
    def __call__(self, str_ref, **kwargs):
        if str_ref is None:
            return
        assert isinstance(str_ref, str)
        ref = RecipeReference.loads(str_ref)
        req = Requirement(ref, **kwargs)
        if self._requires.get(req):
            raise ConanException("Duplicated requirement: {}".format(ref))
        self._requires[req] = req

    def build_require(self, ref, raise_if_duplicated=True, package_id_mode=None, visible=False,
                      run=None, options=None, override=None):
        """
             Represent a generic build require, could be a tool, like "cmake" or a bundle of build
             scripts.

             visible = False => Only the direct consumer can see it, won't conflict
             build = True => They run in the build machine (e.g cmake)
             libs = False => We won't link with it, is a tool, no propagate the libs.
             headers = False => We won't include headers, is a tool, no propagate the includes.
             run = None => It will be determined by the package_type of the ref
        """
        pass

    def test_require(self, ref, run=None, options=None, force=None):
        """
             Represent a testing framework like gtest

             visible = False => Only the direct consumer can see it, won't conflict
             build = False => The test are linked in the host context to run in the host machine
             libs = True => We need to link with gtest
             headers = True => We need to include gtest.
             run = None => It will be determined by the package_type of ref, maybe is gtest shared
        """
        pass

    def tool_require(self, ref, raise_if_duplicated=True, package_id_mode=None, visible=False,
                     run=True, options=None, override=None):
        """
         Represent a build tool like "cmake".

         visible = False => Only the direct consumer can see it, won't conflict
         build = True => They run in the build machine (e.g cmake)
         libs = False => We won't link with it, is a tool, no propagate the libs.
         headers = False => We won't include headers, is a tool, no propagate the includes.
        """
        pass

    def __repr__(self):
        return repr(self._requires.values())

    def serialize(self):
        pass

    def __len__(self):
        return len(self._requires)
