from pathlib import Path
import subprocess
import shutil
import os

SERVICES = Path("/services/")

class Plugin:
    """Base class for all add-ons. This class should not be initialized directly; use subclasses."""

    def __init__(self, name: str, logo: str | Path, repo: str, version: str, folder_name: str):
        self.name = name
        self.logo = logo
        self.repo = repo
        self.folder_name = folder_name
        self.version = version
        self.is_installed = False
        self.stats = {}

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


class InstalledPlugin(Plugin):
    def __init__(self, name, logo, repo, version):
        super().__init__(name, logo, repo, version)
        self.is_installed = True
        self.is_enabled = False
        self.stats = {
            "status": "unknown",
            "cpu": "unknown",
            "memory": "unknown",
            "disk": "unknown"
        }
        self.path = Path(f"/opt/spiriRobotUI/plugins/{self.name}")
        self.description = "No description provided"

    def run(self):
        if self.is_enabled:
            try:
                subprocess.run(['docker', 'compose', '-f', 'docker-compose.yaml', 'up', '-d'],
                            check=True, cwd=Path(self.path))
            except subprocess.CalledProcessError as e:
                print(f"Failed: {e}")
            print(f"{self.name} is running")
        else:
            print(f"Error: {self.name} is not enabled")

    def stop(self):
        if self.is_enabled:
            self.is_enabled = False
            print(f"{self.name} stopped")
        else:
            print(f"Error: {self.name} is not enabled")
    
    def uninstall(self):
        if self.is_enabled:
            print(f"Error: {self.name} is enabled. Please disable it before uninstalling.")
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

    def enable(self):
        if not self.is_enabled:
            # call get_stats()
            self.is_enabled = True
            print(f"{self.name} enabled")
        else:
            print(f"Error: {self.name} already enabled")

    def disable(self):
        if self.is_enabled:
            self.is_enabled = False
            print(f"{self.name} disabled")
        else:
            print(f"Error: {self.name} not enabled")

    def get_stats(self):
        status = "calculate status here"
        cpu = "calculate cpu here"
        memory = "calculate memory here"
        disk = "calulate disk here"
        self.stats["status"] = status
        self.stats["cpu"] = cpu
        self.stats["memory"] = memory
        self.stats["disk"] = disk
        return self.stats

    def get_status(self):
        print("fetching and returning status")
        return self.stats["status"]

    def get_cpu(self):
        cores = "command to fetch number of cpu cores"
        used = "command to fetch amount used, type float"
        total = "command to fetch total amount, type float"
        notes = "calulations will likely happen to convert into optimal size unit"
        print("Calculating and returning CPU usage (cores/used/total)")
        return self.stats["cpu"]

    def get_memory(self):
        used = "command to fetch amount used, type float"
        total = "command to fetch total amount, type float"
        notes = "calulations will likely happen to convert into optimal size unit"
        print("Calculating and returning memory usage (used/total)")
        return self.stats["memory"]

    def get_disk(self):
        used = "command to fetch amount used, type float"
        total = "command to fetch total amount, type float"
        notes = "calulations will likely happen to convert into optimal size unit"
        print("Calculating and returning disk usage (used/total)")
        return self.stats["disk"]
