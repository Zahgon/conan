import os


def bazel_layout(conanfile, src_folder=".", build_folder=".", target_folder=None):
    """Bazel layout is so limited. It does not allow to create its special symlinks in other
    folder. See more information in https://bazel.build/remote/output-directories"""
    pass
