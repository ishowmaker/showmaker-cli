import os
from pathlib import Path

from chaser_util import config


def test_config_dir_with_xdg_config_home(monkeypatch):
    monkeypatch.setenv("CHASER_CONFIG_HOME", "/path/to/config")
    assert config.config_dir() == "/path/to/config"


def test_config_dir_without_xdg_config_home(monkeypatch, mocker):
    monkeypatch.delenv("CHASER_CONFIG_HOME", raising=False)
    home_path = Path("/home/user") if os.name != 'nt' else Path("C:/Users/user")
    mocker.patch.object(Path, 'home', return_value=home_path)
    expected_path = str(home_path / ".config")
    assert config.config_dir() == expected_path
