from conan.tools.apple.apple import to_apple_arch, xcodebuild_deployment_target_key
from conan.tools.build import cmd_args_to_string


class XcodeBuild:
    def __init__(self, conanfile):
        self._conanfile = conanfile
        self._build_type = conanfile.settings.get_safe("build_type")
        self._arch = to_apple_arch(self._conanfile)
        self._sdk = conanfile.settings.get_safe("os.sdk") or ""
        self._sdk_version = conanfile.settings.get_safe("os.sdk_version") or ""
        self._os = conanfile.settings.get_safe("os")
        self._os_version = conanfile.settings.get_safe("os.version")

    @property
    def _verbosity(self):
        pass

    @property
    def _sdkroot(self):
        # User's sdk_path has priority, then if specified try to compose sdk argument
        # with sdk/sdk_version settings, leave blank otherwise and the sdk will be automatically
        # chosen by the build system
        pass

    def build(self, xcodeproj, target=None, configuration=None, cli_args=None):
        """
        Call to ``xcodebuild`` to build a Xcode project.

        :param xcodeproj: the *xcodeproj* file to build.
        :param target: the target to build, in case this argument is passed to the ``build()``
                       method it will add the ``-target`` argument to the build system call. If not passed, it
                       will build all the targets passing the ``-alltargets`` argument instead.
        :param configuration: Build configuration to use (e.g., ``Debug``, ``Release``).
                              Defaults to the recipe's ``settings.build_type``.
        :param cli_args: Extra options to pass directly to ``xcodebuild`` (list of strings).
                              Examples: ``["-xcconfig", "<path/to/file.xcconfig>"]`` or custom
                              Xcode build settings like ``["BUILD_LIBRARY_FOR_DISTRIBUTION=YES"]``.
        :return: the return code for the launched ``xcodebuild`` command.
        """
        pass
