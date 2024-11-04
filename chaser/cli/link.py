import typer

from .app import get_app_list, get_current_app_id, link_app
from .choices import choices_select
from .access_token_cache import token_cache, Region


def link():
    """
    Link the project to an app.
    :return:
    """
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first.")
        return
    apps = get_app_list(access_token)
    if len(apps) == 0:
        typer.echo("No apps found. Please create an app at https://connectdev.io first.")

    current_app_id = get_current_app_id(".")
    if not current_app_id:
        typer.echo("No app linked to the project yet.")
    selected = _select_app(apps, current_app_id)
    typer.echo(f"Switching to app: {selected['name']} ...")
    link_app(".", selected['appId'])


def _select_app(app_list, current_app_id):
    current_app = [app for app in app_list if app["appId"] == current_app_id]
    if len(current_app) > 0:
        typer.echo(f"Current app: {current_app[0]['name']}")
    typer.echo("Please select an app:")

    for idx, app in enumerate(app_list):
        typer.echo(f"{idx + 1}. {app['name']}")

    selected = choices_select(app_list)
    if selected:
        return selected
    else:
        typer.echo("No app selected.")
