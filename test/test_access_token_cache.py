import pytest
from unittest import mock
from tempfile import NamedTemporaryFile
from chaser.cli.access_token_cache import AccessTokenCache, Region
import json


@pytest.fixture(scope="function")
def temp_file():
    file = NamedTemporaryFile(delete=False)
    file.close()
    return file.name


@pytest.fixture(scope="function")
def access_token_cache(temp_file):
    with mock.patch("chaser.cli.access_token_cache.AccessTokenCache.FILE_PATH", temp_file):
        yield AccessTokenCache()


def test_load_empty_cache(temp_file, access_token_cache):
    assert access_token_cache.load() == {}


def test_load_existing_cache(temp_file, access_token_cache):
    cache_data = {
        "us": "us_token",
        "cn": "cn_token"
    }
    with open(temp_file, "w") as file:
        file.write(json.dumps(cache_data))

    assert access_token_cache.load() == cache_data


def test_add_new_token(access_token_cache):
    region = Region.US
    access_token = "new_token"

    access_token_cache.add(access_token, region)
    assert access_token_cache.access_token_cache[region.value] == access_token


def test_add_existing_token(access_token_cache):
    region = Region.CN
    existing_token = "existing_token"
    access_token_cache.access_token_cache[region] = existing_token

    access_token_cache.add(existing_token, region)
    assert access_token_cache.access_token_cache[region] == existing_token


def test_save_cache(temp_file, access_token_cache):
    cache_data = {
        "us": "us_token",
        "cn": "cn_token"
    }
    access_token_cache.access_token_cache = cache_data

    access_token_cache.save()
    with open(temp_file, "r") as file:
        saved_data = json.load(file)

    assert saved_data == cache_data


@mock.patch("chaser.cli.access_token_cache.json.dump")
def test_save_cache_error(mock_dump, access_token_cache):
    mock_dump.side_effect = Exception("Failed to save cache")

    access_token_cache.save()
    assert mock_dump.called
