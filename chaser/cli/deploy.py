import time

import requests
import typer
from requests import RequestException
from rich import print
import tempfile
import os
from .runtime import detect_runtime
from chaser_util.archive import create_zip_archive
from .constants import CHASER_BASE_URL
from .app import get_current_app_id
from .access_token_cache import token_cache, Region


def deploy(
        m: str = typer.Option(help="The deploy message."),
        project_dir: str = typer.Option(default=".", help="The project directory.")):
    """
    Deploy the project.
    """
    print("Deploying the project ...")
    print(f"Deploy message: {m}")
    access_token = token_cache.get(Region.US)
    if access_token is None:
        typer.echo("Please login first.")
        return

    rt, error = detect_runtime(project_dir)
    if error is not None:
        typer.echo("Failed to detect runtime.", error)
        return

    archive_file_path = _package_project(project_dir, rt.name)
    current_app_id = get_current_app_id(".")
    if current_app_id is None:
        typer.echo("No app linked to the project yet.")
        return
    typer.echo(f"Current app id: {current_app_id}")
    _deploy_local_file_remote(current_app_id, 1, archive_file_path, m, access_token)
    pass


def _package_project(project_path: str, name: str):
    rt,error = detect_runtime(project_path)
    if error is not None:
        typer.echo("Failed to detect runtime.", error)
        return
    fileDir = tempfile.mkdtemp(prefix="chaser")
    archiveFilePath = os.path.join(fileDir, "chaser.zip")
    create_zip_archive(project_path, archiveFilePath, name)
    print(f"Project packaged at {archiveFilePath}")
    return archiveFilePath


def _deploy_local_file_remote(app_id: str, env: int, archive_file_path: str, message: str, access_token: str):
    print(f"Deploying to remote server ...")
    print(f"App id: {app_id} env: {env} archive_file_path: {archive_file_path} message: {message}")
    files = {'zip': open(archive_file_path, 'rb')}
    headers = {'APP-ID': app_id,
               'Authorization': f'Bearer {access_token}'}
    json_data = {'message': message, 'comment': message, 'async': True}

    url = CHASER_BASE_URL + "/groups/web/envs/{}/version".format(env)
    response = requests.post(url, headers=headers, data=json_data, files=files)
    response.raise_for_status()
    event_token = response.json()["eventToken"]
    ok, err = _poll_events(app_id, event_token)
    if err:
        return err
    if not ok:
        return Exception("Deploy failed.")


def _poll_events(app_id, token):
    headers = {
        "APP-ID": app_id,
    }

    from_time = ""
    ok = True
    retry_count = 0
    while True:
        time.sleep(0.7)
        url = f"{CHASER_BASE_URL}/events/poll/{token}"
        if from_time != "":
            url += f"?from={from_time}"

        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
        except RequestException as err:
            retry_count += 1
            if retry_count > 3:
                return False, err
            continue

        event = resp.json()

        for i in range(len(event["events"]) - 1, -1, -1):
            e = event["events"][i]
            ok = e["level"].lower() != "error"
            from_time = e["time"]
            if ok:
                print("[REMOTE] " + e["content"] + "\r\n")
            else:
                print("[REMOTE] " + "[ERROR] " + e["content"] + "\r\n")

        if not event["moreEvent"]:
            break

    return ok, None
