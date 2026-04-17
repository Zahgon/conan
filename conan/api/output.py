import fnmatch
import os
import sys
import time
from threading import Lock

import colorama
from colorama import Fore, Style

from conan.errors import ConanException

LEVEL_QUIET = 80  # -q
LEVEL_ERROR = 70  # Errors
LEVEL_WARNING = 60  # Warnings
LEVEL_NOTICE = 50  # Important messages to attract user attention.
LEVEL_STATUS = 40  # Default - The main interesting messages that users might be interested in.
LEVEL_VERBOSE = 30  # -v  Detailed informational messages.
LEVEL_DEBUG = 20  # -vv Closely related to internal implementation details
LEVEL_TRACE = 10  # -vvv Fine-grained messages with very low-level implementation details


class Color:
    """ Wrapper around colorama colors that are undefined in importing
    """
    RED = Fore.RED  # @UndefinedVariable
    WHITE = Fore.WHITE  # @UndefinedVariable
    CYAN = Fore.CYAN  # @UndefinedVariable
    GREEN = Fore.GREEN  # @UndefinedVariable
    MAGENTA = Fore.MAGENTA  # @UndefinedVariable
    BLUE = Fore.BLUE  # @UndefinedVariable
    YELLOW = Fore.YELLOW  # @UndefinedVariable
    BLACK = Fore.BLACK  # @UndefinedVariable

    BRIGHT_RED = Style.BRIGHT + Fore.RED  # @UndefinedVariable
    BRIGHT_BLUE = Style.BRIGHT + Fore.BLUE  # @UndefinedVariable
    BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW  # @UndefinedVariable
    BRIGHT_GREEN = Style.BRIGHT + Fore.GREEN  # @UndefinedVariable
    BRIGHT_CYAN = Style.BRIGHT + Fore.CYAN  # @UndefinedVariable
    BRIGHT_WHITE = Style.BRIGHT + Fore.WHITE  # @UndefinedVariable
    BRIGHT_MAGENTA = Style.BRIGHT + Fore.MAGENTA  # @UndefinedVariable


if os.environ.get("CONAN_COLOR_DARK"):
    Color.WHITE = Fore.BLACK
    Color.CYAN = Fore.BLUE
    Color.YELLOW = Fore.MAGENTA
    Color.BRIGHT_WHITE = Fore.BLACK
    Color.BRIGHT_CYAN = Fore.BLUE
    Color.BRIGHT_YELLOW = Fore.MAGENTA
    Color.BRIGHT_GREEN = Fore.GREEN


def init_colorama(stream):
    pass


def _color_enabled(stream):
    """
    NO_COLOR: No colors

    https://no-color.org/

    Command-line software which adds ANSI color to its output by default should check for the
    presence of a NO_COLOR environment variable that, when present (**regardless of its value**),
    prevents the addition of ANSI color.

    CLICOLOR_FORCE: Force color

    https://bixense.com/clicolors/
    """
    pass


class ConanOutput:
    """ A singleton class to handle output messages in Conan.

    Recipes should only access this class through the ``self.output`` attribute of the recipe,
    but custom commands or tools can instantiate it directly, where doing so for each message is
    a valid practice.

    It provides methods to write messages at different levels of verbosity, such as debug, info,
    warning, and error. The output level can be controlled by the user through command-line options
    or environment variables.

    The output methods return the instance itself, so different methods can be chained together.
    """
    # Singleton
    _conan_output_level = LEVEL_STATUS
    _silent_warn_tags = []
    _warnings_as_errors = []
    lock = Lock()

    def __init__(self, scope: str = ""):
        """ Initialize the ConanOutput instance.

        :parameter scope: A string that represents the scope of the output. This is usually the
            reference of the recipe being executed, like ``pkg/1.0@user/channel`` and is prefixed
            to the output messages. If not provided, it defaults to an empty string.
        """
        self.stream = sys.stderr
        self._scope = scope
        # FIXME:  This is needed because in testing we are redirecting the sys.stderr to a buffer
        #         stream to capture it, so colorama is not there to strip the color bytes
        self._color = _color_enabled(self.stream)

    @classmethod
    def define_silence_warnings(cls, warnings):
        pass

    @classmethod
    def set_warnings_as_errors(cls, value):
        pass

    @classmethod
    def get_output_level(cls):
        pass

    @classmethod
    def set_output_level(cls, level):
        pass

    @classmethod
    def valid_log_levels(cls):
        pass

    @classmethod
    def define_log_level(cls, v):
        pass

    @classmethod
    def level_allowed(cls, level):
        pass

    @property
    def color(self):
        pass

    @property
    def scope(self):
        pass

    @scope.setter
    def scope(self, out_scope):
        pass

    @property
    def is_terminal(self):
        pass

    def writeln(self, data, fg=None, bg=None):
        pass

    def write(self, data, fg=None, bg=None, newline=False):
        pass

    def box(self, msg: str):
        """ Draw a box around the message, useful for important messages"""
        pass

    def login_msg(self, msg, newline=False):
        # unconditional to the error level, this has to show always
        pass

    def _write_message(self, msg, fg=None, bg=None, newline=True):
        pass

    def trace(self, msg: str):
        """ This is the most extreme level of detail.

        Trace messages log every little step the system takes, including function entries and exits,
        variable changes, and other very specific events.

        This message won't be printed unless the user has set the log level to trace
        (e.g., using the ``-vvv`` option in the command line).

        It’s used when full visibility of everything happening in the system is required,
        but should be used carefully due to the large amount of information it can generate."""
        pass

    def debug(self, msg: str, fg: str = Color.MAGENTA, bg: str = None):
        """ With a high level of detail, it is mainly used for debugging code.

        This message won't be printed unless the user has set the log level to debug
        (e.g., using the ``-vv`` option in the command line).

        These messages provide useful information for developers, such as variable values
        or execution flow details, to trace errors or analyze the program's behavior."""
        pass

    def verbose(self, msg: str, fg: str = None, bg: str = None):
        """ Displays additional and detailed information that, while not critical,
        can be useful for better understanding how the system is working.

        This message won't be printed unless the user has set the log level to verbose
        (e.g., using the ``-v`` option in the command line).

        It’s appropriate for gaining more context without overloading the logs with
        excessive detail. Useful when more clarity is needed than a simple info."""
        pass

    def status(self, msg: str, fg: str = None, bg: str = None, newline: bool = True):
        """ Provides general information about the system or ongoing operations.

        Info messages are basic and used to inform about common events,
        like the start or completion of processes, without implying specific problems or achievements."""
        pass

    info = status

    def title(self, msg: str):
        """ Draws a title around the message, useful for important messages"""
        pass

    def subtitle(self, msg: str):
        """ Draws a subtitle around the message, useful for important messages"""
        pass

    def highlight(self, msg: str):
        """ Marks or emphasizes important events or processes that need to stand out but don’t necessarily
        indicate success or error.

        These messages draw attention to key points that may be relevant for the user or administrator."""
        pass

    def success(self, msg: str):
        """ Shows that an operation has been completed successfully.

        This type of message is useful to confirm that key processes or tasks have finished correctly,
        which is essential for good application monitoring."""
        pass

    @staticmethod
    def _warn_tag_matches(warn_tag, patterns):
        pass

    def warning(self, msg: str, warn_tag: str = None):
        """ Highlights a potential issue that, while not stopping the system,
        could cause problems in the future or under certain conditions.

        Warnings signal abnormal situations that should be
        reviewed but don’t necessarily cause an immediate halt in operations.
        Notice that if the tag matches the pattern in the ``core:warnings_as_errors`` configuration,
        and is not skipped, this will be upgraded to an error, and raise an exception
        when the output is printed, so that the error does not pass unnoticed."""
        pass

    def error(self, msg: str, error_type: str = None):
        """ Indicates that a serious issue has occurred that prevents the system
        or application from continuing to function correctly.

        Typically, this represents a failure in the normal flow of execution,
        such as a service crash or a critical exception.
        Notice that if the user has set the ``core:warnings_as_errors`` configuration,
        this will raise an exception when the output is printed,
        so that the error does not pass unnoticed."""
        pass

    def flush(self):
        pass


def cli_out_write(data, fg=None, bg=None, endline="\n", indentation=0):
    """
    Output to be used by formatters to dump information to stdout
    """
    pass


class TimedOutput:
    def __init__(self, interval, out=None, msg_format=None):
        self._interval = interval
        self._msg_format = msg_format
        self._t = time.time()
        self._out = out or ConanOutput()

    def info(self, msg, *args, **kwargs):
        pass
