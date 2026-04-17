from conan.errors import ConanException
from conan.internal.model.recipe_ref import ref_matches

_falsey_options = ["false", "none", "0", "off", ""]


def option_not_exist_msg(option_name, existing_options):
    """ Someone is referencing an option that is not available in the current package
    options
    """
    pass


class _PackageOption:
    def __init__(self, name, value, possible_values=None):
        self._name = name
        self._value = value  # Value None = not defined
        self.important = False
        # possible_values only possible origin is recipes
        if possible_values is None:
            self._possible_values = None
        else:
            # This can contain "ANY"
            self._possible_values = [str(v) if v is not None else None for v in possible_values]

    def dumps(self, scope=None):
        pass

    def copy_conaninfo_option(self):
        # To generate a copy without validation, for package_id info.options value
        pass

    def __bool__(self):
        if self._value is None:
            return False
        return self._value.lower() not in _falsey_options

    def __str__(self):
        return str(self._value)

    def __int__(self):
        return int(self._value)

    def _check_valid_value(self, value):
        """ checks that the provided value is allowed by current restrictions
        """
        pass

    def __eq__(self, other):
        # To promote the other to string, and always compare as strings
        # if self.options.myoption == 1 => will convert 1 to "1"
        if other is None:
            return self._value is None
        other = str(other)
        self._check_valid_value(other)
        if self._value is None:
            return False  # Other is not None here
        return other == self.__str__()

    @property
    def name(self):
        pass

    @property
    def value(self):
        pass

    @value.setter
    def value(self, v):
        pass

    def validate(self):
        # check that this has a valid option value defined
        pass


class _PackageOptions:
    def __init__(self, recipe_options_definition=None):
        if recipe_options_definition is None:
            self._constrained = False
            self._data = {}
        else:
            self._constrained = True
            self._data = {str(option): _PackageOption(str(option), None, possible_values)
                          for option, possible_values in recipe_options_definition.items()}
        self._freeze = False

    def dumps(self, scope=None):
        pass

    @property
    def possible_values(self):
        pass

    def update(self, options):
        """
        @type options: _PackageOptions
        """
        # Necessary for init() extending of options for python_requires_extend
        for k, v in options._data.items():
            self._data[k] = v

    def clear(self):
        # for header_only() clearing
        pass

    def freeze(self):
        pass

    def __contains__(self, option):
        return str(option) in self._data

    def get_safe(self, field, default=None):
        pass

    def rm_safe(self, field):
        # This should never raise any exception, in any case
        pass

    def validate(self):
        pass

    def copy_conaninfo_options(self):
        # To generate a copy without validation, for package_id info.options value
        pass

    def _ensure_exists(self, field):
        pass

    def __getattr__(self, field):
        assert field[0] != "_", "ERROR %s" % field
        try:
            return self._data[field]
        except KeyError:
            raise ConanException(option_not_exist_msg(field, list(self._data.keys())))

    def __delattr__(self, field):
        assert field[0] != "_", "ERROR %s" % field
        # It is always possible to remove an option, even if it is frozen (freeze=True),
        # and it got a value, because it is the only way an option could be removed
        # conditionally to other option value (like fPIC if shared)
        self._ensure_exists(field)
        del self._data[field]

    def __setattr__(self, field, value):
        if field[0] == "_":
            return super(_PackageOptions, self).__setattr__(field, value)
        self._set(field, value)

    def __setitem__(self, item, value):
        self._set(item, value)

    def _set(self, item, value):
        # programmatic way to define values, for Conan codebase
        pass

    def items(self):
        result = []
        for field, package_option in sorted(list(self._data.items())):
            result.append((field, package_option.value))
        return result

    def update_options(self, other, is_pattern=False):
        """
        @param is_pattern: if True, then the value might not exist and won't be updated
        @type other: _PackageOptions
        """
        pass


class Options:

    def __init__(self, options=None, options_values=None):
        # options=None means an unconstrained/profile definition
        try:
            self._package_options = _PackageOptions(options)
            # Addressed only by name, as only 1 configuration is allowed
            # if more than 1 is present, 1 should be "private" requirement and its options
            # are not public, not overridable
            self._deps_package_options = {}  # {name("Boost": PackageOptions}
            if options_values:
                for k, v in options_values.items():
                    if v is None:
                        continue  # defining a None value means same as not giving value
                    k = str(k).strip()
                    v = str(v).strip()
                    tokens = k.split(":", 1)
                    if len(tokens) == 2:
                        package, option = tokens
                        if not package:
                            raise ConanException("Invalid empty package name in options. "
                                                 f"Use a pattern like `mypkg/*:{option}`")
                        if "/" not in package and "*" not in package and "&" not in package:
                            msg = "The usage of package names `{}` in options is " \
                                  "deprecated, use a pattern like `{}/*:{}` " \
                                  "instead".format(k, package, option)
                            raise ConanException(msg)
                        if "[" in package:
                            msg = (f"Options pattern {package} contains a version range, which has no effect. "
                                   f"Only '&' for consumer and '*' as wildcard are supported in this context.")
                            from conan.api.output import ConanOutput
                            ConanOutput().warning(msg, warn_tag="risk")
                        self._deps_package_options.setdefault(package, _PackageOptions())[option] = v
                    else:
                        self._package_options[k] = v
        except Exception as e:
            raise ConanException("Error while initializing options. %s" % str(e))

    def __repr__(self):
        return self.dumps()

    @property
    def possible_values(self):
        pass

    def dumps(self):
        """ produces a multiline text representation of all values, first self then others.
        In alphabetical order, skipping real None (not string "None") values:
            option1=value1
            other_option=3
            OtherPack:opt3=12.1
        """
        pass

    @staticmethod
    def loads(text):
        """ parses a multiline text in the form produced by dumps(), NO validation here
        """
        pass

    def serialize(self):
        # used by ConanInfo serialization, involved in "list package-ids" output
        # we need to maintain the "options" and "req_options" first level or servers will break
        # This happens always after reading from conaninfo.txt => all str and not None
        pass

    def clear(self):
        # for header_only() clearing
        pass

    def __contains__(self, option):
        return option in self._package_options

    def __getattr__(self, attr):
        return getattr(self._package_options, attr)

    def __setattr__(self, attr, value):
        if attr[0] == "_" or attr == "values":
            return super(Options, self).__setattr__(attr, value)
        return setattr(self._package_options, attr, value)

    def __delattr__(self, field):
        self._package_options.__delattr__(field)

    def __getitem__(self, item):
        if isinstance(item, str):
            if "/" not in item and "*" not in item:  # FIXME: To allow patterns like "*" or "foo*"
                item += "/*"
        return self._deps_package_options.setdefault(item, _PackageOptions())

    def scope(self, ref):
        """ when there are free options like "shared=True", they apply to the "consumer" package
        Once we know the name of such consumer package, it can be defined in the data, so it will
        be later correctly apply when processing options """
        pass

    def copy_conaninfo_options(self):
        # To generate the package_id info.options copy, that can destroy, change and remove things
        pass

    def update(self, options=None, options_values=None):
        # Necessary for init() extending of options for python_requires_extend
        new_options = Options(options, options_values)
        self._package_options.update(new_options._package_options)
        for pkg, pkg_option in new_options._deps_package_options.items():
            self._deps_package_options.setdefault(pkg, _PackageOptions()).update(pkg_option)

    def update_options(self, other):
        """
        dict-like update of options, "other" has priority, overwrite existing
        @type other: Options
        """
        pass

    def apply_downstream(self, down_options, profile_options, own_ref, is_consumer):
        """ compute the current package options, starting from the self defined ones and applying
        the options defined by the downstrream consumers and the profile
        Only modifies the current package_options, not the dependencies ones
        """
        pass

    def get_upstream_options(self, down_options, own_ref, is_consumer):
        """ compute which options should be propagated to the dependencies, a combination of the
        downstream defined default_options with the current default_options ones. This happens
        at "configure()" time, while building the graph. Also compute the minimum "self_options"
        which is the state that a package should define in order to reproduce
        """
        pass
