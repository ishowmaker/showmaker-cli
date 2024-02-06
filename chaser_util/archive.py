from __future__ import with_statement

from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os
import fnmatch

ZIP_FILE_MODE = "w"


def __get_ignore_list(runtime_name):
    ignore_patterns = {
        "node.js": [".git/", ".DS_Store", "node_modules/"],
        "python": [".git/", ".DS_Store", "venv", "*.pyc", "__pycache__/"],
    }
    return ignore_patterns.get(runtime_name, [])


def __should_ignore(path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(path, pattern) or path.startswith(pattern):
            return True
    return False


def create_zip_archive(base_dir_path, archive_name, runtime_name):
    """
    Create a zip archive from a directory.
    :param base_dir_path:
    :param archive_name:
    :param runtime_name:
    :return:
    """
    assert os.path.isdir(base_dir_path)
    ignore_list = __get_ignore_list(runtime_name)

    with closing(ZipFile(archive_name, ZIP_FILE_MODE, ZIP_DEFLATED)) as target_zip_file:
        for root, dirs, files in os.walk(base_dir_path):
            dirs[:] = [d for d in dirs if not __should_ignore(os.path.join(root, d), ignore_list)]
            for one_file in files:
                absolute_file_name = os.path.join(root, one_file)
                if __should_ignore(absolute_file_name, ignore_list):
                    continue
                zip_file_name = absolute_file_name[len(base_dir_path) + len(os.sep):]
                target_zip_file.write(absolute_file_name, zip_file_name)

    return target_zip_file
