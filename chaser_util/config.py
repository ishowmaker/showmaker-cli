import os
import pathlib


def config_dir() -> str:
    """Returns the user configuration directory."""
    env = os.environ.get("CHASER_CONFIG_HOME")
    if env:
        return env
    return os.path.join(pathlib.Path.home(), ".config")
