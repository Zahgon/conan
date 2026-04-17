from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.model.recipe_ref import ref_matches


class BuildMode:
    """ build_mode => ["*"] if user wrote "--build=*"
                   => ["hello", "bye"] if user wrote "--build hello --build bye"
                   => ["hello/0.1@foo/bar"] if user wrote "--build hello/0.1@foo/bar"
                   => ["!foo"] or ["~foo"] means exclude when building all from sources
    """
    def __init__(self, params):
        self._missing = False
        self._never = False
        self.cascade = False
        self._editable = False
        self._patterns = []
        self._build_missing_patterns = []
        self._build_missing_excluded = []
        self._build_compatible_patterns = []
        self._build_compatible_excluded = []
        self._excluded_patterns = []
        if params is None:
            return

        assert isinstance(params, list)
        assert len(params) > 0  # Not empty list

        for param in params:
            if param == "missing":
                self._missing = True
            elif param == "editable":
                self._editable = True
            elif param == "never":
                self._never = True
            elif param == "cascade":
                self.cascade = True
                ConanOutput().warning("Using build-mode 'cascade' is generally inefficient and it "
                                      "shouldn't be used. Use 'package_id' and 'package_id_modes' "
                                      "for more efficient re-builds")
            else:
                if param.startswith("missing:"):
                    clean_pattern = param[len("missing:"):]
                    if clean_pattern and clean_pattern[0] in ["!", "~"]:
                        self._build_missing_excluded.append(clean_pattern[1:])
                    else:
                        self._build_missing_patterns.append(clean_pattern)
                elif param == "compatible":
                    self._build_compatible_patterns = ["*"]
                elif param.startswith("compatible:"):
                    clean_pattern = param[len("compatible:"):]
                    if clean_pattern and clean_pattern[0] in ["!", "~"]:
                        self._build_compatible_excluded.append(clean_pattern[1:])
                    else:
                        self._build_compatible_patterns.append(clean_pattern)
                else:
                    clean_pattern = param
                    if clean_pattern and clean_pattern[0] in ["!", "~"]:
                        self._excluded_patterns.append(clean_pattern[1:])
                    else:
                        self._patterns.append(clean_pattern)

            if self._never and (self._missing or self._patterns or self.cascade):
                raise ConanException("--build=never not compatible with other options")

    @property
    def editable(self):
        # we can make this conditional on the context in the future
        pass

    def forced(self, conan_file, ref, with_deps_to_build=False):
        # TODO: ref can be obtained from conan_file

        pass

    def allowed(self, conan_file):
        pass

    def allowed_compatible(self, conanfile):
        pass

    def should_build_missing(self, conanfile):
        pass
