import os
import json

from conan.api.output import ConanOutput
from conan.errors import ConanException
from conan.internal.cache.conan_reference_layout import METADATA
from conan.internal.cache.home_paths import HomePaths
from conan.internal.loader import load_python_file
from conan.internal.util.files import load, mkdir, save, sha256sum


PKGSIGN_MANIFEST = "pkgsign-manifest.json"
PKGSIGN_SIGNATURES = "pkgsign-signatures.json"


def _save_manifest(artifacts_folder, signature_folder):
    """
    Creates the summary content as a dictionary for manipulation.

    Returns a structure like:
        {
            "files": [
                {"file": "conan_package.tgz", "sha256": "abc123"},
                {"file": "other_file.bin", "sha256": "fff999"},
                pass
            ]
        }
    """
    pass


def _save_signatures(signature_folder, signatures):
    """
    Saves the content of signatures file in the signature folder
    :param signature_folder: Signature folder path
    :param signatures: dict of {filename: signature_value}
    """
    pass


def _verify_files_checksums(signature_folder, files):
    """
    Verifies that the files' checksums match those stored in the summary.
    :param signature_folder: Signature folder path
    :param files: dict of {filename: filepath} of files in artifact folder to verify
    """
    pass


class PkgSignaturesPlugin:
    def __init__(self, cache, home_folder):
        self._cache = cache
        signer = HomePaths(home_folder).sign_plugin_path
        if os.path.isfile(signer):
            mod, _ = load_python_file(signer)
            self._plugin_sign_function = getattr(mod, "sign", None)
            self._plugin_verify_function = getattr(mod, "verify", None)
        else:
            self._plugin_sign_function = self._plugin_verify_function = None

    @property
    def is_sign_configured(self):
        pass

    @property
    def is_verify_configured(self):
        pass

    def sign_pkg(self, ref, files, folder):
        pass

    def sign(self, upload_data):
        pass

    def verify(self, ref, folder, metadata_folder, files):
        pass
