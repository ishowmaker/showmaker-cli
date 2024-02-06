import os
import shutil
import zipfile


def is_dir(path: str) -> bool:
    return os.path.sep == path[-1]


def extract_and_write_file(info: zipfile.ZipInfo, zf: zipfile.ZipFile, dest_path: str):
    path = os.path.join(dest_path, info.filename)
    if info.filename.endswith("/"):
        os.makedirs(path, exist_ok=True)
    else:
        with zf.open(info) as f_in, open(path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
