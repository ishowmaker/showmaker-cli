import platform

import typer
from rich import print

from .app import get_current_app_id, get_app_info
from .runtime import detect_runtime
from .access_token_cache import token_cache, Region


def start(project_path: str = typer.Option(help="The project path."),
          port: str = typer.Option(default=3000, help="The port to run the project.")):
    """
    local start the project.
    :param project_path:
    :param port:
    :return:
    """
    if project_path:
        print(f"Project path: {project_path}")
    else:
        project_path = "."

    _print_system_info()
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first.")
        return
    app_id = get_current_app_id(".")
    print("Retrieving app info ...")
    app = get_app_info(app_id, access_token)
    print(f"Current app: [bold red] {app['name']} [/bold red] {app['appId']}")
    rt, error = detect_runtime(project_path)
    if error is not None:
        typer.echo("Failed to detect runtime.", error)
        return
    rt.run(port)


def _print_system_info():
    pt = platform.uname()
    print(f"System info: {pt.system} {pt.machine}")
