from pathlib import Path
import subprocess
import shutil
import os
import docker
import git

SERVICES = Path("/services/")

class Plugin:
    """Base class for all plugins"""

    def __init__(self, name: str, logo: str | Path, repo: str, folder_name: str):
        self.name = name
        self.logo = logo
        self.repo = repo
        self.folder_name = folder_name
        self.is_installed = False

    def install(self):
        if not self.is_installed:
            try:
                if os.path.exists(SERVICES/self.folder_name):
                    print(f"Error: {self.name} already installed.")
                    return

                shutil.copytree(f"/robot-config-ui/repos/{self.repo}/services/{self.folder_name}", SERVICES/self.folder_name)
            except shutil.Error as e:
                print(f"Error copying folder: {e}")
            except OSError as e:
                print(f"OS Error: {e}")
            self.is_installed = True
            print(f"{self.name} installed")
        else:
            print(f"Error: {self.name} already installed")  # This method should be overridden in subclasses

    def uninstall(self):
        if self.is_installed:
            try:
                shutil.rmtree(SERVICES / self.folder_name)
            except OSError as e:
                print(f"Error removing folder: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            self.is_installed = False
            print(f"{self.name} uninstalled")
        else:
            print(f"Error: {self.name} not installed")

class InstalledPlugin(Plugin):

    def __init__(self, name, logo, repo, folder_name):
        super().__init__(name, logo, repo, folder_name)
        self.is_installed = True
        self.is_running = False
        self.base_stats = {}
        self.current_stats = {}

    def run(self):
        if not self.is_running:
            try:
                subprocess.run(['docker', 'compose', 'up'],
                            check=True, cwd=Path(SERVICES / self.folder_name))
            except subprocess.CalledProcessError as e:
                print(f"Failed: {e}")
            self.is_running = True
            print(f"{self.name} is running")
        else:
            print(f"Error: {self.name} is already running")

    def stop(self):
        if self.is_running:
            try:
                subprocess.run(['docker', 'compose', 'down'],
                            check=True, cwd=Path(SERVICES / self.folder_name))
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
            self.delete_plugin()

    def get_logs(self):
        if self.is_running:
            print(f"Fetching logs for {self.name}")
            try:
                client = docker.from_env()
                container = client.containers.get(self.folder_name)
                logs = container.logs().decode('utf-8')
                print(logs)
            except docker.errors.NotFound:
                print(f"Error: Container '{self.folder_name}' not found.")
            except docker.errors.APIError as e:
                print(f"Error interacting with Docker API: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print(f"Error: {self.name} is not running. Cannot fetch logs.")

    def download_logs(self):
        if self.is_enabled:
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
            
    def configure(self, config: dict):
        if self.is_enabled:
            print(f"Configuring {self.name} with provided settings")
            # Implement configuration logic here
        else:
            print(f"Error: {self.name} is not enabled. Cannot configure.")

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

        def delete_plugin(self):
            print(f"Deleting {self.name} plugin")
