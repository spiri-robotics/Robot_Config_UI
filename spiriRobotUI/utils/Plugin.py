from pathlib import Path
import subprocess
import shutil
import docker
import git
from nicegui import ui
from spiriRobotUI.settings import PROJECT_ROOT
from spiriRobotUI.utils.EventBus import event_bus
from loguru import logger
import time
import asyncio

SERVICES = Path("/services/")

installed_plugins = {}


class Plugin:
    """Base class for all plugins"""

    def __init__(self, name: str, logo: str | Path, repo: str, folder_name: str):
        self.name = name
        self.logo = logo
        self.url = ""
        self.repo = repo
        self.folder_name = folder_name
        self.is_installed = False
        self.is_running = False
        self.readme_contents = self.get_readme_contents()

    def install(self):
        if not self.is_installed:
            try:
                dest_path = SERVICES / self.folder_name
                if dest_path.exists():
                    print(f"Error: {self.name} already installed.")
                    self.is_installed = True
                    if self.name in installed_plugins:
                        print(f"{self.name} is already in installed plugins.")
                    else:
                        installed_plugins[self.name] = InstalledPlugin(
                            self.name, self.logo, self.repo, self.folder_name
                        )
                    return

                app_path = Path("repos") / self.repo / "services" / self.folder_name
                print(f"Installing {self.name} from {app_path}")
                shutil.copytree(app_path, SERVICES / self.folder_name)

                # Add a default .env if one doesn't exist in the destination
                env_file = SERVICES / self.folder_name / ".env"
                if not env_file.exists():
                    with open(env_file, "w") as f:
                        f.write("# Default environment variables\n")
            except shutil.Error as e:
                print(f"Error copying folder: {e}")
            except OSError as e:
                print(f"OS Error: {e}")
            installed_plugins[self.name] = InstalledPlugin(
                self.name, self.logo, self.repo, self.folder_name
            )
            self.is_installed = True
            print(f"{self.name} installed")
        else:
            print(f"Error: {self.name} already installed")
        event_bus.emit("plugin_installed", self.name)

    def uninstall(self):
        if self.is_installed:
            try:
                shutil.rmtree(SERVICES / self.folder_name)
            except OSError as e:
                print(f"Error removing folder: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            installed_plugins.pop(self.name, None)
            self.is_installed = False
            print(f"{self.name} uninstalled")
        else:
            print(f"Error: {self.name} not installed")
        event_bus.emit("plugin_uninstalled", self.name)

    def get_readme_contents(self):
        path = f"repos/{self.repo}/services/{self.name}/README.md"
        if Path(path).exists():
            with open(path, "r") as f:
                readme_contents = f.read()
            return readme_contents
        else:
            return ""


plugins = {}

for repo in (PROJECT_ROOT / "repos").iterdir():
    for plugin in (PROJECT_ROOT / "repos" / repo.name / "services").iterdir():
        logo = (
            PROJECT_ROOT / "repos" / repo.name / "services" / plugin.name / "logo.jpg"
        )
        if not logo.exists():
            logo = "spiriRobotUI/icons/cat_icon.jpg"
        plugins[plugin.name] = Plugin(plugin.name, str(logo), repo.name, plugin.name)


class InstalledPlugin(Plugin):

    def __init__(self, name, logo, repo, folder_name):
        super().__init__(name, logo, repo, folder_name)
        self.is_installed = True
        self.containers = []
        client = docker.from_env()
        containers = client.containers.list(all=True)
        for container in containers:
            if self.folder_name in container.name:
                self.containers.append(container)
        if len(self.containers) > 0:
            self.is_running = True
        else:
            self.is_running = False
        self.current_stats = {
            "status": "stopped",
            "cpu": 0.0,
            "memory": 0.0,
            "disk": 0.0,
        }

    async def run(self):
        print(f"Running {self.name}...")
        if not self.is_running:
            try:
                subprocess.Popen(
                    ["docker", "compose", "up", "-d"],
                    cwd=Path(SERVICES / self.folder_name),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                await asyncio.sleep(2)
                # Find and assign the new container
                self.containers.clear()  # Clear previous containers
                client = docker.from_env()
                containers = client.containers.list(all=True)
                for container in containers:
                    if self.folder_name in container.name:
                        self.containers.append(container)
                if len(self.containers) == 0:
                    print(f"No running containers found for {self.folder_name}")
            except subprocess.CalledProcessError as e:
                print(f"Failed: {e}")
                return
            except FileNotFoundError:
                print(
                    "Error: Docker Compose not found. Please ensure Docker is installed and running."
                )
                return
            self.is_running = True
            event_bus.emit("plugin_run", self.name)
            print(f"{self.name} is running")
        else:
            print(f"Error: {self.name} is already running")

    async def stop(self):
        if self.is_running:
            try:
                subprocess.Popen(
                    ["docker", "compose", "down"],
                    cwd=Path(SERVICES / self.folder_name),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except subprocess.CalledProcessError as e:
                print(f"Failed: {e}")

            while True:
                try:
                    self.container.reload()  # Refresh container status
                    status = self.container.status
                    if status == "exited" or status == "stopped":
                        break
                except docker.errors.NotFound:
                    # Container has been removed, consider it stopped
                    break
                except Exception as e:
                    logger.error(f"Error checking container status: {e}")
                    break
                time.sleep(1)
                logger.debug(f"Waiting for container to stop... {status}")

            self.is_running = False
            self.container = None
            event_bus.emit("plugin_run", self.name)
            print(f"{self.name} stopped")
        else:
            print(f"Error: {self.name} is not running")

    def uninstall(self):
        if self.is_running:
            ui.notify(
                f"Error: {self.name} is running. Please stop it before uninstalling."
            )
        else:
            super().uninstall()

    def get_logs(self):
        if self.is_running:
            print(f"Fetching logs for {self.name}")
            try:
                self.containers.clear()  # Clear previous containers
                client = docker.from_env()
                containers = client.containers.list(all=True)
                for container in containers:
                    if self.folder_name in container.name:
                        self.containers.append(container)
                logs = self.container.logs().decode("utf-8")
                log_file_path = Path(PROJECT_ROOT) / "logs.txt"
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"\n--- Logs for {self.name} ---\n")
                    log_file.write(logs)
                    log_file.write("\n")
                return logs
            except docker.errors.NotFound:
                print(f"Error: Container '{self.folder_name}' not found.")
            except docker.errors.APIError as e:
                print(f"Error interacting with Docker API: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print(f"Error: {self.name} is not running. Cannot fetch logs.")

    def update(self):
        if self.is_installed:
            repo_path = str(PROJECT_ROOT) + "/repos/" + self.repo

            try:
                # Load the repository object
                repo = git.Repo(repo_path)

                # Get the 'origin' remote (or specify a different remote if needed)
                origin = repo.remote(name="origin")

                # Perform the pull operation
                pull_info = origin.pull()

                print(f"Successfully pulled changes from origin. Details: {pull_info}")

            except git.InvalidGitRepositoryError:
                print(f"Error: '{repo_path}' is not a valid Git repository.")
            except Exception as e:
                print(f"An error occurred during git pull: {e}")
        else:
            print(f"Error: {self.name} is not installed. Cannot update.")

    def get_compose_file(self):
        compose_file_path = Path(SERVICES / self.folder_name / "docker-compose.yml")
        if compose_file_path.exists():
            with open(compose_file_path, "r") as file:
                return file.read()
        else:
            print(f"Error: Docker Compose file not found at {compose_file_path}")
            return "File not found"

    def get_env(self):
        env_file_path = Path(SERVICES / self.folder_name / ".env")
        if env_file_path.exists():
            with open(env_file_path, "r") as file:
                return file.read()
        else:
            print(f"Error: .env file not found at {env_file_path}")
            return ""

    def set_env(self, env_text):
        env_file_path = Path(SERVICES / self.folder_name / ".env")
        try:
            with open(env_file_path, "w") as file:
                file.write(env_text)
            print(f"Environment variables updated for {self.name}")
        except Exception as e:
            print(f"Error updating .env file: {e}")

    def get_current_stats(self):
        if not self.is_running:
            print(f"{self.name} is not running. Cannot fetch stats.")
            return
        client = docker.from_env()
        containers = client.containers.list(all=True)
        found = False
        for container in containers:
            if self.folder_name in container.name:
                self.container = container
                found = True
                break
        if not found or not self.container:
            print(f"No running container found for {self.folder_name}")
            return
        try:
            stats = self.container.stats(stream=False)
            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )
            system_delta = (
                stats["cpu_stats"]["system_cpu_usage"]
                - stats["precpu_stats"]["system_cpu_usage"]
            )
            cpu_percent = 0.0
            if system_delta > 0 and cpu_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * len(
                    stats["cpu_stats"]["cpu_usage"]["percpu_usage"]
                )
            self.current_stats["cpu"] = cpu_percent
            self.current_stats["memory"] = stats["memory_stats"]["usage"] / (1024**2)
            self.current_stats["memory_limit"] = stats["memory_stats"]["limit"] / (
                1024**2
            )
            self.current_stats["disk"] = 10  # Placeholder
            self.current_stats["status"] = self.container.status
        except Exception as e:
            print(f"Error fetching stats: {e}")

    async def update_stats_periodically(self):
        while self.is_running:
            self.get_current_stats()
            await asyncio.sleep(1)


# Scan the SERVICES directory and register installed plugins.
for service_dir in SERVICES.iterdir():
    if service_dir.is_dir():
        for plugin in plugins.values():
            if (
                service_dir.name == plugin.folder_name
                and plugin.name not in installed_plugins
            ):
                plugin.is_installed = True
                installed_plugins[plugin.name] = InstalledPlugin(
                    plugin.name, plugin.logo, plugin.repo, plugin.folder_name
                )
