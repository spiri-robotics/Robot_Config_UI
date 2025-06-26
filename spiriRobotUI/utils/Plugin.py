from pathlib import Path
import subprocess
import shutil
import os
import docker
import git
from spiriRobotUI.settings import PROJECT_ROOT

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
                    if  self.name in installed_plugins:
                        print(f"{self.name} is already in installed plugins.")
                    else:
                        installed_plugins[self.name] = InstalledPlugin(
                            self.name,
                            self.logo,
                            self.repo,
                            self.folder_name
                        )
                    return
                
                app_path = Path("repos") / self.repo / "services" / self.folder_name
                print(f"Installing {self.name} from {app_path}")
                shutil.copytree(app_path, SERVICES/self.folder_name)
            except shutil.Error as e:
                print(f"Error copying folder: {e}")
            except OSError as e:
                print(f"OS Error: {e}")
            installed_plugins[self.name] = InstalledPlugin(
                self.name,
                self.logo,
                self.repo,
                self.folder_name
            )
            self.is_installed = True
            print(f"{self.name} installed")
        else:
            print(f"Error: {self.name} already installed")  

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

    def get_readme_contents(self):
        path = f"repos/{self.repo}/services/{self.name}/README.md"
        if Path(path).exists():
            with open(path, "r") as f:
                readme_contents = f.read()
            return readme_contents
        else:
            return ""
        
plugins = {
    "plugin1": Plugin(
        "plugin1",
        "spiriRobotUI/icons/cat_icon.jpg",
        "robot-config-test-repo",
        "webapp-example"
    )
}

class InstalledPlugin(Plugin):

    def __init__(self, name, logo, repo, folder_name):
        super().__init__(name, logo, repo, folder_name)
        self.is_installed = True
        self.is_running = False
        self.base_stats = {"cores": 0, "memory": 0, "disk": 0}
        self.current_stats = {"status": "stopped", "cpu": 0.0, "memory": 0.0, "disk": 0.0}
        self.container = None

    def run(self):
        print(f"Running {self.name}...")
        if not self.is_running:
            try:
                subprocess.Popen(['docker', 'compose', 'up'],
                            cwd=Path(SERVICES / self.folder_name), 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print(f"Failed: {e}")
            self.is_running = True
            print(f"{self.name} is running")
        else:
            print(f"Error: {self.name} is already running")

    def stop(self):
        if self.is_running:
            try:
                subprocess.Popen(['docker', 'compose', 'down'],
                            cwd=Path(SERVICES / self.folder_name), 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print(f"Failed: {e}")
            self.is_running = False
            print(f"{self.name} stopped")
        else:
            print(f"Error: {self.name} is not running")
    
    def uninstall(self):
        if self.is_running:
            print(f"Error: {self.name} is running. Please stop it before uninstalling.")
        else:
            super().uninstall()

    def get_logs(self):
        if self.is_running:
            print(f"Fetching logs for {self.name}")
            try:
                client = docker.from_env()
                containers = client.containers.list(all=True)
                for container in containers:
                    if self.folder_name in container.name:
                        self.container = container
                logs = self.container.logs().decode('utf-8')
                return logs
            except docker.errors.NotFound:
                print(f"Error: Container '{self.folder_name}' not found.")
            except docker.errors.APIError as e:
                print(f"Error interacting with Docker API: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print(f"Error: {self.name} is not running. Cannot fetch logs.")

    def download_logs(self):
        if self.is_running:
            print(f"Downloading logs for {self.name}")
            try:
                client = docker.from_env()
                container = client.containers.get(self.folder_name)
                logs = container.logs().decode('utf-8')

                with open(f"{self.folder_name}_logs.txt", 'w') as f:
                    f.write(logs)
                print(f"Logs for container '{self.folder_name}' saved to '{self.folder_name}_logs.txt'")

            except docker.errors.NotFound:
                print(f"Error: Container '{self.folder_name}' not found.")
            except docker.errors.APIError as e:
                print(f"Error interacting with Docker API: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            else:
                print(f"Error: {self.name} is not enabled. Cannot download logs.")
    
    def update(self):
        if self.is_installed:
            repo_path = "/path/to/your/local/repo"

            try:
                # Load the repository object
                repo = git.Repo(repo_path)

                # Get the 'origin' remote (or specify a different remote if needed)
                origin = repo.remote(name='origin')

                # Perform the pull operation
                pull_info = origin.pull()

                print(f"Successfully pulled changes from origin. Details: {pull_info}")

            except git.InvalidGitRepositoryError:
                print(f"Error: '{repo_path}' is not a valid Git repository.")
            except Exception as e:
                print(f"An error occurred during git pull: {e}")
        else:
            print(f"Error: {self.name} is not installed. Cannot update.")

    def display_compose_file(self):
        compose_file_path = Path(SERVICES / self.folder_name / 'docker-compose.yml')
        if compose_file_path.exists():
            with open(compose_file_path, 'r') as file:
                content = file.read()
                print(f"Contents of {compose_file_path}:\n{content}")
        else:
            print(f"Error: Docker Compose file not found at {compose_file_path}")
            
    def edit_env(self, config: dict):
        print(f"Configuring {self.name} with provided settings")

    def get_base_stats(self):
        cores = 16.0  # fetch cores here
        memory = 128.0  # fetch total memory here
        disk = 128.0  # fetch total disk space here
        self.base_stats["cores"] = cores
        self.base_stats["memory"] = memory
        self.base_stats["disk"] = disk

    def get_current_stats(self):
        status =  "running"
        if not self.is_running:
            status = "stopped"
        cpu =  0.0 # fetch current CPU usage here
        memory = 0.0  # fetch current memory usage here
        disk = 0.0  # fetch current disk usage here
        self.current_stats["status"] = status
        self.current_stats["cpu"] = cpu 
        self.current_stats["memory"] = memory
        self.current_stats["disk"] = disk