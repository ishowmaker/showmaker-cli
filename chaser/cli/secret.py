import requests
import typer
from .app import get_current_app_id
from .access_token_cache import token_cache, Region
from .constants import CHASER_BASE_URL


def set_secret(
        secret_name: str = typer.Argument(..., help="Name of the secret"),
        value: str = typer.Argument(..., help="KeyValue to set for the secret"),
):
    """
    Example: secret set SECRET_KEY  SECRET_VALUE
    :param secret_name:
    :param value:
    :return:
    """
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first")
        return
    typer.echo(f"Setting secret '{secret_name}' with key value '{value}'")
    current_app_id = get_current_app_id(".")
    typer.echo(f"Current app id: {current_app_id}")
    envs, err = _get_environments(current_app_id, access_token)
    if err:
        typer.echo(err)
        return
    envs[secret_name] = value
    err = _put_environments(current_app_id, envs, access_token)
    if err:
        typer.echo(err)
        return
    typer.echo(f"Secret '{secret_name}' set successfully")


def unset_secret(
        secret_name: str = typer.Argument(..., help="Name of the secret"),
):
    """
    Example: secret unset SECRET_KEY
    :param secret_name:
    :return:
    """
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first")
        return
    typer.echo(f"unsetting secret '{secret_name}'")
    current_app_id = get_current_app_id(".")
    typer.echo(f"Current app id: {current_app_id}")
    envs, err = _get_environments(current_app_id, access_token)
    if err:
        typer.echo(err)
        return
    if secret_name not in envs:
        typer.echo(f"Secret '{secret_name}' not found")
        return
    envs.pop(secret_name)
    err = _put_environments(current_app_id, envs, access_token)
    if err:
        typer.echo(err)
        return
    typer.echo(f"Secret '{secret_name}' unset successfully")


def list_secret(
):
    """
    Example: secret list
    :return:
    """
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first")
        return
    current_app_id = get_current_app_id(".")
    typer.echo(f"Current app id: {current_app_id}")
    envs, err = _get_environments(current_app_id, access_token)
    if err:
        typer.echo(err)
        return
    if len(envs) == 0:
        typer.echo("No secrets found.")
        return
    for key, value in envs.items():
        typer.echo(f"{key}={value}")


def _put_environments(app_id, envs, access_token):
    headers = {
        'APP-ID': app_id,
        'Authorization': f'Bearer {access_token}',
    }

    params = {
        "environments": envs
    }

    url = f"{CHASER_BASE_URL}/groups/web"
    response = requests.patch(url, json=params, headers=headers)

    if response.status_code != 200:
        return f"Error updating environment variable, code: {response.status_code}"
    return None


def _get_environments(app_id, access_token):
    headers = {
        'APP-ID': app_id,
        'Authorization': f'Bearer {access_token}',
    }

    url = f"{CHASER_BASE_URL}/groups?all=true"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None, f"Error getting environment variable, code: {response.status_code}"

    return response.json()[0]["environments"], None
