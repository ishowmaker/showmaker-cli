
from chaser_util.env import environ


def test_environ():
    environment = environ()

    assert isinstance(environment, list)

    for env in environment:
        assert isinstance(env, str)
        assert '=' in env
