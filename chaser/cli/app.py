import errno
import http
import json
import os

import requests
import typer

from .constants import API_BASE_URL


def get_app_list(access_token):
    """
    Get a list of apps from the server.
    """

    url = _get_apps_list_url()
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    params = {
        'page': 1,
        'page_size': 50,
    }

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == http.HTTPStatus.UNAUTHORIZED.value:
        typer.echo("Login failed: Unauthorized! Please login in first.")
    resp.raise_for_status()
    data = json.loads(resp.text)
    return data['list']


def _get_apps_list_url():
    return API_BASE_URL + "/api/client/apps"


def link_app(project_path: str, app_id: str) -> None:
    """
    Link the app to the project.
    :param project_path:
    :param app_id:
    :return:
    """
    app_dir_path = _app_dir_path(project_path)
    _create_directory(app_dir_path)

    current_app_id_file_path = _current_app_id_file_path(project_path)
    _write_to_file(current_app_id_file_path, app_id)


def _app_dir_path(project_path: str) -> str:
    return os.path.join(project_path, ".chaser")


def _create_directory(directory_path: str) -> None:
    try:
        os.makedirs(directory_path, mode=0o775)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def _write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)


def get_current_app_id(project_path):
    """
    Get the current app id.
    :param project_path:
    :return:
    """
    file_path = _current_app_id_file_path(project_path)
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError as e:
        return None
    except Exception as e:
        raise ValueError(str(e))


def _current_app_id_file_path(project_path: str) -> str:
    return os.path.join(_app_dir_path(project_path), "current_app_id")


def get_app_info(app_id, access_token):
    """
    Get the app info.
    :param app_id:
    :param access_token:
    :return:
    """

    url = _get_app_info_url(app_id)
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(url, headers=headers)
    if resp.status_code == http.HTTPStatus.UNAUTHORIZED.value:
        typer.echo("Login failed: Unauthorized! Please login in first.")
        raise Exception(f"Failed to get app info: {resp.text}")
    resp.raise_for_status()
    return json.loads(resp.text)


def _get_app_info_url(app_id: str) -> str:
    return API_BASE_URL + "/api/client/app/" + app_id
