from conan.internal.graph.graph import CONTEXT_BUILD
from conan.errors import ConanException
from conan.internal.model.recipe_ref import ref_matches


def initialize_conanfile_profile(conanfile, profile_build, profile_host, base_context,
                                 is_build_require, ref=None, parent=None):
    """ this function fills conanfile information with the profile informaiton
    It is called for:
        - computing the root_node
           - GraphManager.load_consumer_conanfile, for "conan source" command
           - GraphManager._load_root_consumer for "conan install <path to conanfile>
           - GraphManager._load_root_test_package for "conan create ." with test_package folder
        - computing each graph node:
            GraphBuilder->create_new_node
    """
    pass


def _per_package_settings(conanfile, profile, ref):
    # Prepare the settings for the loaded conanfile
    # Mixing the global settings with the specified for that name if exist
    pass


def _initialize_conanfile(conanfile, profile, settings, ref):
    pass


def consumer_definer(conanfile, profile_host, profile_build):
    """ conanfile.txt does not declare settings, but it assumes it uses all the profile settings
    These settings are very necessary for helpers like generators to produce the right output
    """
    pass
