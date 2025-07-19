import asyncio, docker, git, shutil, subprocess, time, re, random

from pathlib import Path
from nicegui import ui
from loguru import logger

from spiriRobotUI.settings import PROJECT_ROOT
from spiriRobotUI.utils.EventBus import event_bus

SERVICES = Path("/services/")
REPOS = PROJECT_ROOT / 'repos'
if not REPOS.exists():
    REPOS.mkdir()

plugins = {}
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
                        compose_file = SERVICES / self.folder_name / "docker-compose.yaml"
                        if not compose_file.exists():
                            compose_file = SERVICES / self.folder_name / "docker-compose.yml"
                            if not compose_file.exists():
                                ui.notify(f"{compose_file} not found!", type="error")
                        compose_text = compose_file.read_text()
                        variables = set(re.findall(r'\$[{]?([A-Z_][A-Z0-9_]*)[}]?', compose_text))

                        for var in variables:
                            logger.debug(f"Detected variable: {var}")
                            f.write(f"{var}=\n")
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
            if self.is_running:
                ui.notify('Please disable plugin before uninstalling', type='negative')
                return False
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

class InstalledPlugin(Plugin):

    def __init__(self, name, logo, repo, folder_name):
        super().__init__(name, logo, repo, folder_name)
        self.is_installed = True
        self._containers = []
        self.update_containers()
        if len(self._containers) > 0:
            self.is_running = True
        else:
            self.is_running = False
        self.current_stats = {
            "status": "stopped",
            "cpu": 0.0,
            "memory": 0.0,
            "disk": 0.0,
        }

    def update_containers(self):
        self._containers.clear()
        client = docker.from_env()
        containers = client.containers.list(all=True)
        for container in containers:
            if self.folder_name in container.name:
                self._containers.append(container)

    def get_random_stats(self):
        self.current_stats["cpu"] = random.randint(0, 100)
        self.current_stats["memory"] = random.randint(0, 100)
        self.current_stats["memory_limit"] = 100
        self.current_stats["disk"] = 10  # Placeholder
        
    def get_status(self):
        if not self.is_running:
            return "stopped"
        self.update_containers()
        if len(self._containers) == 0:
            return "Loading..."
        container_states = [c.status for c in self._containers]
        states = {
            "Running": container_states.count("running"),
            "Restarting": container_states.count("restarting"),
            "Exited": container_states.count("exited"),
            "Created": container_states.count("created"),
            "Paused": container_states.count("paused"),
            "Dead": container_states.count("dead")
        }
        return states
    
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
                self.update_containers()
                if len(self._containers) == 0:
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
            plugins[self.name].is_running = True
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
                all_stopped = True
                try:
                    self.update_containers()  # Refresh container list
                    for container in self._containers:
                        container.reload()
                        status = container.status
                        if status not in ("exited", "stopped"):
                            all_stopped = False
                            break
                except docker.errors.NotFound:
                    # Container has been removed, continue checking others
                    pass
                except Exception as e:
                    logger.error(f"Error checking container status: {e}")
                    break
                if all_stopped or len(self._containers) == 0:
                    break
                time.sleep(1)
                logger.debug("Waiting for containers to stop...")

            self.is_running = False
            plugins[self.name].is_running = False
            self._containers = []
            event_bus.emit("plugin_run", self.name)
            print(f"{self.name} stopped")
        else:
            print(f"Error: {self.name} is not running")

    def uninstall(self):
        if self.is_running:
            ui.notify(f"Please disable plugin before uninstalling", type='negative')
        else:
            super().uninstall()

    def get_logs(self):
        if self.is_running:
            print(f"Fetching logs for {self.name}")
            try:
                self.update_containers()
                logs_list = {}
                for i in range(0, len(self._containers)):
                    logs = self._containers[i].logs().decode("utf-8")
                    log_dir = Path(PROJECT_ROOT) / 'logs'
                    if log_dir.exists():
                        for file in log_dir.iterdir():
                            if file.is_file():
                                file.unlink()
                            elif file.is_dir():
                                shutil.rmtree(file)
                    log_dir.mkdir(parents=True, exist_ok=True)  # Ensure logs directory exists
                    log_file_path = log_dir / f"{self._containers[i].name}.txt"
                    with open(log_file_path, "w") as log_file:
                        log_file.write(f"\n--- Logs for {self._containers[i].name} ---\n")
                        log_file.write(logs)
                        log_file.write("\n")
                    logs_list[self._containers[i].name] = logs
                return logs_list
            except docker.errors.NotFound:
                print(f"Error: Container '{self.folder_name}' not found.")
                return {}
            except docker.errors.APIError as e:
                print(f"Error interacting with Docker API: {e}")
                return {}
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return {}
        else:
            print(f"Error: {self.name} is not running. Cannot fetch logs.")
            return {}

    def update(self):
        if self.is_installed:
            if self.repo is None:
                print(f"Error: {self.name} does not have a repository to update from.")
                return
            repo_path = str(PROJECT_ROOT) + "/repos/" + self.repo

            try:
                # Load the repository object
                repo = git.Repo(repo_path)

                # Get the 'origin' remote (or specify a different remote if needed)
                origin = repo.remote(name="origin")

                # Perform the pull operation
                pull_info = origin.pull()

                app_path = Path(repo_path) / "services" / self.folder_name
                dest_path = SERVICES / self.folder_name
                # Remove the existing destination directory if it exists
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                # Copy updated files over
                shutil.copytree(app_path, dest_path)

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
        self.update_containers()
        if len(self._containers) == 0:
            print(f"No running container found for {self.folder_name}")
            return
        total_cpu = 0.0
        total_memory = 0.0
        total_memory_limit = 0.0
        status = "running"
        try:
            for container in self._containers:
                if container.status != "running":
                    continue
                stats = container.stats(stream=False)
                
                #CPU Stats
                try:
                    cpu_stats = stats['cpu_stats']
                    precpu_stats = stats['precpu_stats']
                    
                    cpu_usage = cpu_stats['cpu_usage']['total_usage']
                    precpu_usage = precpu_stats['cpu_usage']['total_usage']
                    
                    system_cpu_usage = cpu_stats['system_cpu_usage']
                    pre_system_cpu_usage = precpu_stats['system_cpu_usage']
                    
                    # percpu_usage = cpu_usage['percpu_usage']
                    
                    cpu_delta = cpu_usage - precpu_usage
                    system_delta = system_cpu_usage - pre_system_cpu_usage
                    cpu_percent = 0.0
                    # if system_delta > 0 and cpu_delta > 0 and percpu_usage != null:
                    #     cpu_percent = (cpu_delta / system_delta) * len(percpu_usage)
                    # else:
                    cpu_percent = (cpu_delta / system_delta) * 100
                    total_cpu += cpu_percent
                    
                except Exception as e:
                    total_cpu=0
                    logger.error(f'e')
                   
                #Memory Stats 
                try:
                    memory_stats = stats['memory_stats']
                    total_memory += memory_stats['usage'] / (1024**3)
                    total_memory_limit += memory_stats['limit'] / (1024**3)
                except Exception as e:
                    total_memory=0
                    total_memory_limit =0
                    logger.error(f'e')

                # If any container is not running, mark status as not running
                if container.status != "running":
                    status = container.status

            self.current_stats["cpu"] = total_cpu
            self.current_stats["memory"] = total_memory
            self.current_stats["memory_limit"] = total_memory_limit
            self.current_stats["disk"] = 10  # Placeholder
            self.current_stats["status"] = status
        except Exception as e:
            print(f"Error fetching stats: {e}")

    async def update_stats_periodically(self):
        while self.is_running:
            self.get_current_stats()
            await asyncio.sleep(1)
