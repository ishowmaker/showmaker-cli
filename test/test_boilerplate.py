import os
import tempfile
import zipfile

import pytest
from .helper import is_dir,extract_and_write_file


@pytest.fixture(scope="function")
def zip_file():
    # create a zip file with a single file named "test.txt"
    zip_name = "test.zip"
    with open(zip_name, "wb") as fh:
        with zipfile.ZipFile(fh, mode="w") as zf:
            zf.writestr("test.txt", b"Hello, World!")
            zf.writestr("test_directory/", b"")
    yield zip_name
    os.remove(zip_name)


def test_extract_and_write_file(zip_file):
    with zipfile.ZipFile(zip_file, mode="r") as zf:
        infos = zf.infolist()
        assert len(infos) == 2

        # test directory extraction
        info_dir = infos[1]
        temp_dir = tempfile.TemporaryDirectory()
        extract_and_write_file(info_dir, zf, temp_dir.name)
        assert os.path.exists(os.path.join(temp_dir.name, info_dir.filename))
        assert os.path.isdir(os.path.join(temp_dir.name, info_dir.filename))

        # test file extraction
        info_file = infos[0]
        temp_dir = tempfile.TemporaryDirectory()
        extract_and_write_file(info_file, zf, temp_dir.name)
        assert os.path.exists(os.path.join(temp_dir.name, info_file.filename))
        assert os.path.isfile(os.path.join(temp_dir.name, info_file.filename))
        with open(os.path.join(temp_dir.name, info_file.filename), "rb") as f:
            assert f.read() == b"Hello, World!"

