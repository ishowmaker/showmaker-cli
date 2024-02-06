import os
import tempfile
import zipfile
from typing import Optional, Dict, Callable, List

import progressbar
import requests
import typer
from pydantic import BaseModel
from termcolor import colored

BASE_URL = "https://api.github.com/repos"


class Boilerplate(BaseModel):
    name: str
    download_url: str
    message: Optional[str] = ""


boilerplates = [
    Boilerplate(
        name="Python - Flask",
        download_url="/ishowmaker/python-getting-started/zipball/main",
        message="Flask's documentation at https://flask.palletsprojects.com"
    ),
    Boilerplate(
        name="Go - Echo",
        download_url="/ishowmaker/golang-getting-started/zipball/main",
        message="Lean how to use Echo at https://echo.labstack.com/"
    ),
]


def create_project(boil: Boilerplate, dest: str):
    if boil.download_url != "":
        if not os.path.exists(dest):
            os.makedirs(dest, mode=0o775)

        d = tempfile.mkdtemp(prefix="chaser")
        zip_file_path = os.path.join(d, "getting-started.zip")

        try:
            _download_to_file(BASE_URL + boil.download_url, zip_file_path)
        except:
            raise ValueError("Failed to download %s" % boil.name)

        typer.echo("Creating project...")

        if not os.path.isfile(zip_file_path):
            raise FileNotFoundError("ZIP file does not exist.")

        with zipfile.ZipFile(zip_file_path, "r") as zip_file:
            for f in zip_file.namelist():
                file_name = f.split("/")[-1]
                dest_file = os.path.join(dest, file_name)

                try:
                    zip_file.extract(f, dest)

                    if os.path.isfile(dest_file):
                        os.chmod(dest_file, 0o644)
                except Exception as e:
                    return str(e)

    typer.echo("Created %s project in `%s`" % (boil.name, dest))

    if boil.message != "":
        typer.echo(boil.message)


def _download_to_file(url, file_name):
    resp = requests.get(url)
    resp.raise_for_status()
    with open(file_name, "wb") as fd:
        total_size = int(resp.headers.get('content-length', 0))

        if total_size > 0:
            bar = progressbar.ProgressBar(
                widgets=[colored("[INFO]", "green"), " Downloading templates", progressbar.Bar(),
                         progressbar.Percentage()])
            bar.start()

            bytes_written = 0

            for chunk in resp.iter_content(chunk_size=1024):
                fd.write(chunk)
                bytes_written += len(chunk)
                bar.update(bytes_written * 100 // total_size)

            bar.finish()
        else:
            for chunk in resp.iter_content(chunk_size=1024):
                fd.write(chunk)
