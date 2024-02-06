import typer
from .app import get_current_app_id, get_app_info
from .access_token_cache import token_cache, Region


def info():
    """
    Show the current app info.
    :return:
    """
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first.")
        raise typer.Exit(1)
    current_app_id = get_current_app_id(".")
    if not current_app_id:
        typer.echo("No app linked to the project yet. Please run  link' first")
        raise typer.Exit(1)
    app = get_app_info(current_app_id, access_token)
    typer.echo(f"App name: {app['name']}")
    typer.echo(f"App id: {app['appId']}")
