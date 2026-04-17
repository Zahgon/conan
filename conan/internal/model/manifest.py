import os
from collections import defaultdict

from conan.internal.paths import CONAN_MANIFEST, COMPRESSIONS, PACKAGE_FILE_NAME, EXPORT_FILE_NAME, \
    EXPORT_SOURCES_FILE_NAME
from conan.internal.util.dates import timestamp_now, timestamp_to_str
from conan.internal.util.files import load, md5, md5sum, save, gather_files


class FileTreeManifest:

    def __init__(self, the_time, file_sums):
        """file_sums is a dict with filepaths and md5's: {filepath/to/file.txt: md5}"""
        self.time = the_time
        self.file_sums = file_sums

    def files(self):
        pass

    @property
    def summary_hash(self):
        pass

    @staticmethod
    def loads(text):
        """ parses a string representation, generated with __repr__
        """
        pass

    @staticmethod
    def load(folder):
        pass

    def __repr__(self):
        # Used for serialization and saving it to disk
        ret = ["%s" % self.time]
        for file_path, file_md5 in sorted(self.file_sums.items()):
            ret.append("%s: %s" % (file_path, file_md5))
        ret.append("")
        content = "\n".join(ret)
        return content

    def __str__(self):
        """  Used for displaying the manifest in user readable format in Uploader, when the server
        manifest is newer than the cache one (and not force)
        """
        ret = ["Time: %s" % timestamp_to_str(self.time)]
        for file_path, file_md5 in sorted(self.file_sums.items()):
            ret.append("%s, MD5: %s" % (file_path, file_md5))
        ret.append("")
        content = "\n".join(ret)
        return content

    def save(self, folder, filename=CONAN_MANIFEST):
        pass

    def report_summary(self, output, suffix="Copied"):
        pass

    @classmethod
    def create(cls, folder, exports_sources_folder=None):
        """ Walks a folder and create a FileTreeManifest for it, reading file contents
        from disk, and capturing current time
        """
        pass

    def __eq__(self, other):
        """ Two manifests are equal if file_sums
        """
        return self.file_sums == other.file_sums

    def difference(self, other):
        pass
