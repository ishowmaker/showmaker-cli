from setuptools import setup, find_packages

setup(
    name="connectdev",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer~=0.9.0",
        "rich~=13.6.0",
        "requests~=2.31.0",
        "urllib3~=2.0.7",
        "pydantic~=2.4.2",
        "progressbar~=2.5",
        "termcolor~=2.3.0",
        "click~=8.1.7",
        "grequests~=0.7.0",
        "gevent~=23.9.1",
    ],
    extras_require={
        'dev': [
            "pyinstaller~=6.3.0",
            "pytest~=7.4.2",
            "pytest-mock~=3.12.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'connectdev=chaser.__main__:main',
        ],
    },
    author="ConnectDev",
    author_email="support@connectdev.io",
    description="Command-line tool for ConnectDev which is a platform that lets you host backends for your AI applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://connectdev.io",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
