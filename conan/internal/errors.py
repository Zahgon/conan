import traceback
from contextlib import contextmanager

from conan.errors import ConanException, ConanInvalidConfiguration


@contextmanager
def conanfile_remove_attr(conanfile, names, method):
    """ remove some self.xxxx attribute from the class, so it raises an exception if used
    within a given conanfile method
    """
    pass


@contextmanager
def conanfile_exception_formatter(conanfile, funcname):
    """
    Decorator to throw an exception formatted with the line of the conanfile where the error ocurrs.
    """
    pass


def scoped_traceback(header_msg, exception, scope):
    """
    It will iterate the traceback lines, when it finds that the source code is inside the users
    conanfile it "start recording" the messages, when the trace exits the conanfile we return
    the traces.
    """
    pass


class ConanReferenceDoesNotExistInDB(ConanException):
    """ Reference does not exist in cache db """
    pass


class ConanReferenceAlreadyExistsInDB(ConanException):
    """ Reference already exists in cache db """
    pass


class ConanConnectionError(ConanException):
    pass


class InternalErrorException(ConanException):
    """
         Generic 500 error
    """
    pass


class RequestErrorException(ConanException):
    """
         Generic 400 error
    """
    pass


class AuthenticationException(ConanException):  # 401
    """
        401 error
    """
    pass


class ForbiddenException(ConanException):  # 403
    """
        403 error
    """
    pass


class NotFoundException(ConanException):  # 404
    """
        404 error
    """
    pass


class RecipeNotFoundException(NotFoundException):

    def __init__(self, ref):
        super().__init__(f"Recipe not found: '{ref.repr_notime()}'")


class PackageNotFoundException(NotFoundException):

    def __init__(self, pref):
        super().__init__(f"Binary package not found: '{pref.repr_notime()}'")


EXCEPTION_CODE_MAPPING = {InternalErrorException: 500,
                          RequestErrorException: 400,
                          AuthenticationException: 401,
                          ForbiddenException: 403,
                          NotFoundException: 404,
                          RecipeNotFoundException: 404,
                          PackageNotFoundException: 404}
