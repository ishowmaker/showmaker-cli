import requests
import typer

from .access_token_cache import token_cache, Region
from .constants import API_BASE_URL


def login(
        token: str = typer.Option(help="The token to use for authentication. From Chaser Console => "
                                       "My Account => Personal Token"),
):
    """
    Login to Showmaker.
    """
    typer.echo(f"Starting login with token.")
    try:
        response = _login_with_access_token(token)
        response.raise_for_status()
        token_cache.add(token, Region.US).save()
    except Exception as e:
        typer.echo(f"Login failed: {e}")
        raise typer.Exit(code=1)
    typer.echo("Login succeeded! 🎉")


def _login_with_access_token(access_token: str):
    url = _get_client_login_url()
    headers = {'Authorization': f'Bearer {access_token}'}
    return requests.get(url, headers=headers)


def _get_client_login_url():
    return API_BASE_URL + "/api/client/login"
