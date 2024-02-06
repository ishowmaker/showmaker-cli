import typer

from . import login
from . import new
from . import link
from . import info
from . import start
from . import deploy
from . import secret
from . import logs


def _version_callback(value: bool):
    if value:
        from chaser_version import __version__

        typer.echo(f"chaser client version: {__version__}")
        raise typer.Exit()


entrypoint_cli_typer = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="markdown",
    help="""
    Chaser is the fastest way to run code in the cloud.

    See the website at https://llm.fun for documentation and more information
    about running code on Chaser.
    """,
)


@entrypoint_cli_typer.callback()
def chaser():
    pass


entrypoint_cli_typer.command("login", no_args_is_help=True)(login.login)
entrypoint_cli_typer.command("new", no_args_is_help=False)(new.new_template)
entrypoint_cli_typer.command("link", no_args_is_help=False)(link.link)
entrypoint_cli_typer.command("info", no_args_is_help=False)(info.info)
entrypoint_cli_typer.command("start", no_args_is_help=False)(start.start)
entrypoint_cli_typer.command("deploy", no_args_is_help=False)(deploy.deploy)
entrypoint_cli_typer.command("logs", no_args_is_help=False)(logs.print_log)

secret_app = typer.Typer(name="secret")
entrypoint_cli_typer.add_typer(secret_app, name="secret")
secret_app.command("set", no_args_is_help=False)(secret.set_secret)
secret_app.command("unset", no_args_is_help=False)(secret.unset_secret)
secret_app.command("list", no_args_is_help=False)(secret.list_secret)


if __name__ == "__main__":
    entrypoint_cli_typer()
