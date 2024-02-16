import subprocess
from unittest import mock
from unittest.mock import patch
import pytest
from chaser.cli.runtime import lookup_bin, new_python_runtime


@mock.patch('shutil.which')
def test_lookup_bin_found(mock_which):
    mock_which.return_value = '/usr/bin/python'
    result, error = lookup_bin(['python'])
    assert result == '/usr/bin/python'
    assert error is None


@mock.patch('shutil.which')
def test_lookup_bin_not_found(mock_which):
    mock_which.side_effect = [None] * 3
    with pytest.raises(FileNotFoundError):
        lookup_bin(['python'])


@mock.patch('shutil.which')
def test_lookup_bin_multiple_fallbacks(mock_which):
    mock_which.side_effect = [
        None,
        '/usr/local/bin/python3',
        '/usr/bin/python2'
    ]
    result, error = lookup_bin(['python2', 'python3', 'python'])
    assert result == '/usr/local/bin/python3'
    assert error is None


def test_new_python_runtime_without_python_version_file():
    project_path = "/path/to/project"
    with patch("builtins.open", side_effect=FileNotFoundError):
        runtime, err = new_python_runtime(project_path)

    # Assert that the correct Runtime object is returned
    assert err is None
    assert runtime.command is None
    assert runtime.work_dir == "/path/to/project"
    assert runtime.project_path == "/path/to/project"
    assert runtime.name == "python"
    assert runtime.exec_path == "python"
    assert runtime.args == ["wsgi.py"]
    assert runtime.errors == []


def test_new_python_runtime_with_unexpected_exception():
    project_path = "/path/to/project"
    with pytest.raises(Exception):
        with patch("builtins.open", side_effect=Exception("Some error occurred")):
            new_python_runtime(project_path)
