import errno
import json
import os
import platform
import subprocess, multiprocessing
from rich import print


class Runtime:
    def __init__(self, command, work_dir, project_path, name, exec_path, args=None, envs=None, remote=None, port=None,
                 deploy_files=None, errors=None):
        self.command = command
        self.work_dir = work_dir
        self.project_path = project_path
        self.name = name
        self.exec_path = exec_path
        self.args = args or []
        self.envs = envs or []
        self.remote = remote
        self.port = port
        self.deploy_files = deploy_files
        self.errors = errors or []

    def run(self, port):
        process = multiprocessing.Process(target=run_command, args=(self.exec_path,
                                                                    self.args, self.work_dir, port))
        process.start()
        process.join()


def run_command(exec_path, args, work_dir, port):
    process = subprocess.Popen(
        [exec_path] + args,
        cwd=work_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ,
        universal_newlines=True
    )
    print(f"Use {args} to start the project")
    print("Starting the project ...")
    print(f"The project is running at: http://localhost:{port}")
    process.wait()


def detect_runtime(project_path: str):
    package_file_path = os.path.join(project_path, "package.json")
    if (
            os.path.isfile(os.path.join(project_path, "server.js"))
            and os.path.isfile(package_file_path)
    ):
        print("Node.js runtime detected")
        return new_node_runtime(project_path)

    if os.path.isfile(package_file_path):
        with open(package_file_path) as package_file:
            package_data = json.load(package_file)
            if "scripts" in package_data and "start" in package_data["scripts"]:
                print("Node.js runtime detected")
                return new_node_runtime(project_path)

    if (
            os.path.isfile(os.path.join(project_path, "requirements.txt"))
            and os.path.isfile(os.path.join(project_path, "wsgi.py"))
    ):
        print("Python runtime detected")
        return new_python_runtime(project_path)

    if (
            os.path.isfile(os.path.join(project_path, "index.html"))
            or os.path.isfile(os.path.join(project_path, "static.json"))
    ):
        print("Static runtime detected")
        return new_static_runtime(project_path)

    if os.path.isfile(os.path.join(project_path, "go.mod")):
        print("Go runtime detected")
        return new_go_runtime(project_path)

    return Runtime(None, project_path, project_path, "Unknown", None), "Runtime not found"


def new_node_runtime(project_path: str):
    runtime = Runtime(
        command="node",
        work_dir=project_path,
        project_path=project_path,
        name="node",
        exec_path="/usr/bin/env node",
        args=[],
        errors=[]
    )

    package_json_path = os.path.join(project_path, 'package.json')

    if not os.path.isfile(package_json_path):
        runtime.errors.append('package.json file not found')
        return runtime, None

    try:
        with open(package_json_path, 'r') as f:
            package_json = json.load(f)

            if 'scripts' in package_json and 'start' in package_json['scripts']:
                start_script = package_json['scripts']['start']

                parts = start_script.split(' ')
                runtime.exec_path = parts[0]
                runtime.args = parts[1:]

        return runtime, None

    except Exception as e:
        runtime.errors.append(str(e))
        return runtime, e


def new_static_runtime(project_path):
    return Runtime(
        command=None,
        work_dir=project_path,
        project_path=project_path,
        name="static",
        exec_path="npx",
        args=["serve", "--listen=3000"],
        errors=[]
    ), None


def new_go_runtime(project_path):
    return Runtime(
        command=None,
        work_dir=project_path,
        project_path=project_path,
        name="go",
        exec_path="go",
        args=["run", "main.go"],
        errors=[]
    ), None


def lookup_bin(fallbacks):
    system = platform.system()
    for i, _bin in enumerate(fallbacks):
        bin_path = None
        if system == 'Windows':
            for path in os.environ["PATH"].split(os.pathsep):
                candidate = os.path.join(path, _bin)
                if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                    bin_path = candidate
                    break
        else:
            try:
                bin_path = subprocess.check_output(["which", _bin]).decode().strip()
            except subprocess.CalledProcessError:
                pass

        if bin_path:
            print(f"Found executable file: {bin_path}")
            return bin_path, None
        else:
            if i != len(fallbacks) - 1:
                print(f"Cannot find command {fallbacks[i]}, using {fallbacks[i + 1]} instead")

    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), fallbacks[0])


def new_python_runtime(project_path: str):
    def runtime(version):
        python = "python"
        if version != "":
            parts = version.split(".", 3)
            major, minor = parts[0], parts[1]
            python, _ = lookup_bin(["python" + major + "." + minor, "python" + major, "python"])

        return Runtime(
            command=None,
            work_dir=project_path,
            project_path=project_path,
            name="python",
            exec_path=python,
            args=["wsgi.py"],
            errors=[]
        ), None

    python_version_file = os.path.join(project_path, ".python-version")
    try:
        with open(python_version_file) as f:
            python_version = f.read().strip()
            if python_version.startswith("2.") or python_version.startswith("3."):
                print("pyenv detected. Please make sure pyenv is configured properly.")
                return runtime(python_version)
            else:
                raise ValueError(
                    "Wrong pyenv version. We only support CPython. Please check and correct .python-version")
    except FileNotFoundError:
        return runtime("")
