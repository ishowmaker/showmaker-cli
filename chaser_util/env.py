import os


def environ():
    environment = []

    for key, value in os.environ.items():
        environment.append(f"{key}={value}")

    return environment
