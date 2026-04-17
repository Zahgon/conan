from functools import total_ordering
from typing import Optional

from conan.internal.model.version import Version
from conan.errors import ConanException


@total_ordering
class _Condition:
    def __init__(self, operator, version):
        self.operator = operator
        self.display_version = version

        value = str(version)
        if (operator == ">=" or operator == "<") and "-" not in value and version.build is None:
            value += "-"
        self.version = Version(value)

    def __str__(self):
        return f"{self.operator}{self.display_version}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.operator, self.version))

    def __lt__(self, other):
        # Notice that this is done on the modified version, might contain extra prereleases
        if self.version < other.version:
            return True
        elif self.version == other.version:
            if self.operator == "<":
                if other.operator == "<":
                    return self.display_version.pre is not None
                else:
                    return True
            elif self.operator == "<=":
                if other.operator == "<":
                    return False
                else:
                    return self.display_version.pre is None
            elif self.operator == ">":
                if other.operator == ">":
                    return self.display_version.pre is None
                else:
                    return False
            else:
                if other.operator == ">":
                    return True
                # There's a possibility of getting here while validating if a range is non-void
                # by comparing >= & <= for lower limit <= upper limit
                elif other.operator == "<=":
                    return True
                else:
                    return self.display_version.pre is not None
        return False

    def __eq__(self, other):
        return (self.display_version == other.display_version and
                self.operator == other.operator)


class _ConditionSet:

    def __init__(self, expression, prerelease):
        expressions = expression.split()
        if not expressions:
            # Guarantee at least one expression
            expressions = [""]

        self.prerelease = prerelease
        self.conditions = []
        for e in expressions:
            e = e.strip()
            self.conditions.extend(self._parse_expression(e))

    @staticmethod
    def _parse_expression(expression):
        pass

    def valid(self, version, conf_resolve_prepreleases):
        pass


class VersionRange:
    def __init__(self, expression):
        self._expression = expression
        tokens = expression.split(",")
        prereleases = False
        for t in tokens[1:]:
            if "include_prerelease" in t:
                if "include_prerelease=" in t:
                    from conan.api.output import ConanOutput
                    ConanOutput().warning(
                        f'include_prerelease version range option in "{expression}" does not take an attribute, '
                        'its presence unconditionally enables prereleases')
                prereleases = True
                break
            else:
                t = t.strip()
                if len(t) > 0 and t[0].isalpha():
                    from conan.api.output import ConanOutput
                    ConanOutput().warning(f'Unrecognized version range option "{t}" in "{expression}"')
                else:
                    raise ConanException(f'"{t}" in version range "{expression}" is not a valid option')
        version_expr = tokens[0]
        self.condition_sets = []
        for alternative in version_expr.split("||"):
            self.condition_sets.append(_ConditionSet(alternative, prereleases))

    def __str__(self):
        return self._expression

    def contains(self, version: Version, resolve_prerelease: Optional[bool]):
        """
        Whether <version> is inside the version range

        :param version: Version to check against
        :param resolve_prerelease: If ``True``, ensure prereleases can be resolved in this range
        If ``False``, prerelases can NOT be resolved in this range
        If ``None``, prereleases are resolved only if this version range expression says so
        :return: Whether the version is inside the range
        """
        pass

    def intersection(self, other):
        pass

    def version(self):
        pass


def validate_conan_version(required_range):
    pass
