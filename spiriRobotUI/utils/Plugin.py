from pathlib import Path
import subprocess
import shutil
import os

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
            print(f"{self.name} uninstalled successfully")

    def download_logs(self):
        if self.is_enabled:
            print(f"Downloading logs for {self.name}")
            # Implement log download logic here
        else:
            print(f"Error: {self.name} is not enabled. Cannot download logs.")
    
    def update(self, new_version: str):
        if self.is_installed:
            if new_version != self.version:
                print(f"Updating {self.name} from version {self.version} to {new_version}")
                self.version = new_version
                # Implement update logic here
            else:
                print(f"{self.name} is already at the latest version: {self.version}")
        else:
            print(f"Error: {self.name} is not installed. Cannot update.")

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
        status = "fetch status here"
        cpu = 1.0  # fetch used cpu here
        memory = 1.0  # fetch used memory here
        disk = 1.0  # fetch used disk space here
        self.current_stats["status"] = status
        self.current_stats["cpu"] = cpu
        self.current_stats["memory"] = memory
        self.current_stats["disk"] = disk
