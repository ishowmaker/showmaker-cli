from typing import Optional

import typer
from typing_extensions import Annotated
from .choices import choices_select
from .template import boilerplates, create_project
from .app import get_app_list, link_app
from .access_token_cache import token_cache, Region


def new_template(dest: Annotated[Optional[str], typer.Argument()] = None):
    """
    Create a new project from a template.
    :param dest:
    :return:
    """
    if dest is None:
        dest = "."
    template = _select_template()
    if template is None:
        typer.echo("No template selected.")
        raise typer.Exit(1)
    typer.echo(f"You selected: {template.name}")

    access_token = token_cache.get(Region.US)
    if access_token is None:
        typer.echo("Please login first.")
        return
    apps = get_app_list(access_token)
    if len(apps) == 0:
        typer.echo("No apps found.")
        return

    app = _select_app(apps)
    if app is None:
        typer.echo("No app selected.")
        raise typer.Exit(1)
    typer.echo(f"You selected: {app['name']}")
    create_project(template, dest)
    link_app(dest, app['appId'])


def _select_template():
    typer.echo("Please select an app template:")

    for idx, boil in enumerate(boilerplates):
        typer.echo(f"{idx + 1}. {boil.name}")

    selected_boilerplate = choices_select(boilerplates)
    if selected_boilerplate:
        return selected_boilerplate
    else:
        typer.echo("No template selected.")
        return None


def _select_app(apps):
    typer.echo("Please select an app:")
    for idx, app in enumerate(apps):
        typer.echo(f"{idx + 1}. {app['name']}")

    selected_boilerplate = choices_select(apps)
    if selected_boilerplate:
        return selected_boilerplate
    else:
        typer.echo("No app selected.")
        return None
