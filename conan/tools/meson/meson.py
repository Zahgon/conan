import os

from conan.errors import ConanException
from conan.tools.build import build_jobs
from conan.tools.meson.toolchain import MesonToolchain


class Meson:
    """
    This class calls Meson commands when a package is being built. Notice that
    this one should be used together with the ``MesonToolchain`` generator.
    """

    def __init__(self, conanfile):
        """
        :param conanfile: ``< ConanFile object >`` The current recipe object. Always use ``self``.
        """
        self._conanfile = conanfile

    def configure(self, reconfigure=False):
        """
        Runs ``meson setup [FILE] "BUILD_FOLDER" "SOURCE_FOLDER" [-Dprefix=/]``
        command, where ``FILE`` could be ``--native-file conan_meson_native.ini``
        (if native builds) or ``--cross-file conan_meson_cross.ini`` (if cross builds).

        :param reconfigure: ``bool`` value that adds ``--reconfigure`` param to the final command.
        """
        pass

    def build(self, target=None):
        """
        Runs ``meson compile -C . -j[N_JOBS] [TARGET]`` in the build folder.
        You can specify ``N_JOBS`` through the configuration line ``tools.build:jobs=N_JOBS``
        in your profile ``[conf]`` section.

        :param target: ``str`` Specifies the target to be executed.
        """
        pass

    def install(self, cli_args=None):
        """
        Runs ``meson install -C "." --destdir ..`` in the build folder.

        :param cli_args: List of arguments to be added to the command:
                    ``meson install -C "." --destdir ... arg1 arg2``
        """
        pass

    def test(self):
        """
        Runs ``meson test -v -C "."`` in the build folder.
        """
        pass

    @property
    def _build_verbosity(self):
        # verbosity of build tools. This passes -v to ninja, for example.
        # See https://github.com/mesonbuild/meson/blob/master/mesonbuild/mcompile.py#L156
        pass

    @property
    def _install_verbosity(self):
        # https://github.com/mesonbuild/meson/blob/master/mesonbuild/minstall.py#L81
        # Errors are always logged, and status about installed files is controlled by this flag,
        # so it's a bit backwards
        pass

    @property
    def _prefix(self):
        """Generate a valid ``--prefix`` argument value for meson.
        For conan, the prefix must be similar to the Unix root directory ``/``.

        The result of this function should be passed to
        ``meson setup --prefix={self._prefix} ...``

        Python 3.13 changed the semantics of ``/`` on the Windows ntpath module,
        it is now special-cased as a relative directory.
        Thus, ``os.path.isabs("/")`` is true on Linux but false on Windows.
        So for Windows, an equivalent path is ``C:\\``. However, this can be
        parsed wrongly in meson in specific circumstances due to the trailing
        backslash. Hence, we also use forward slashes for Windows, leaving us
        with ``C:/`` or similar paths.

        See also
        --------
        * The meson issue discussing the need to set ``--prefix`` to ``/``:
            `mesonbuild/meson#12880 <https://github.com/mesonbuild/meson/issues/12880>`_
        * The cpython PR introducing the ``/`` behavior change:
            `python/cpython#113829 <https://github.com/python/cpython/pull/113829>`_
        * The issue detailing the erroneous parsing of ``\\``:
            `conan-io/conan#14213 <https://github.com/conan-io/conan/issues/14213>`_
        """
        pass
