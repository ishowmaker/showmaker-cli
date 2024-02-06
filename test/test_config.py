import pathlib

from chaser_util import config
from pytest_mock import mocker


def test_config_dir_with_xdg_config_home(monkeypatch):
    monkeypatch.setenv("CHASER_CONFIG_HOME", "/path/to/config")
    assert config.config_dir() == "/path/to/config"


def test_config_dir_without_xdg_config_home(monkeypatch, mocker):
    monkeypatch.delenv("CHASER_CONFIG_HOME", raising=False)
    mocker.patch.object(pathlib.Path, 'home', return_value="/home/user")
    assert config.config_dir() == "/home/user/.config"
