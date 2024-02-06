import warnings

warnings.filterwarnings("ignore")

from cli.entry_point import entrypoint_cli_typer


def main():
    entrypoint_cli_typer()


if __name__ == "__main__":
    main()
