import typer
import requests
import time
from .app import get_current_app_id
from .access_token_cache import token_cache, Region
from .constants import CHASER_BASE_URL


def print_log(
        limit: int = typer.Option(10, "--limit", "-l", help="Maximum lines to print"),
        follow: bool = typer.Option(None, "--follow", "-f", help="tail logs"),
):
    """
    Print logs.
    """
    access_token = token_cache.get(Region.US)
    if not access_token:
        typer.echo("Please login first")
        raise typer.Exit(1)
    current_app_id = get_current_app_id(".")
    if not current_app_id:
        typer.echo("No app linked to the project yet. Please run  link' first")
        raise typer.Exit(1)
    typer.echo(f"Current app id: {current_app_id}")
    _receive_logs_by_limit(_json_log_printer, current_app_id, limit, follow, access_token)


def _json_log_printer(log):
    typer.echo(log['content'])


def _fetch_logs(app_id, params, access_token: str):
    url = f"{CHASER_BASE_URL}/logs"
    headers = {
        "APP-ID": app_id,
        'Authorization': f'Bearer {access_token}',
    }

    retry_count = 0
    while True:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            break
        if retry_count >= 3:
            typer.echo("Failed to fetch logs")
            return None, ValueError("Failed to fetch logs")
        retry_count += 1
        time.sleep(1.123)
    return resp.json(), None


def _receive_logs_by_limit(printer, app_id, limit, follow, access_token: str):
    params = {
        "limit": str(limit),
        "prod": "1",
        "groupName": "web"
    }
    while True:
        logs, err = _fetch_logs(app_id, params, access_token)
        if err:
            return err

        for log in reversed(logs):
            error = printer(log)
            if error:
                print(f"error \"{error}\" while parsing log: {log}")
        if not follow:
            break

        params.pop("limit", None)
        if logs:
            params["to"] = logs[0]["time"]
        params["from"] = time.strftime("%Y-%m-%dT%H:%M:%S.000000000Z", time.gmtime())

        time.sleep(5)

    return None
