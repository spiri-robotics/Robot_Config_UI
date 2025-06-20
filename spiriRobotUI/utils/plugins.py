import asyncio
from pathlib import Path


class Plugin:
    """Base class for all add-ons. This class should not be initialized directly; use subclasses."""

    def __init__(self, name: str, logo: str | Path, repo: str, version: str):
        self.name = name
        self.logo = logo
        self.repo = repo
        self.version = version
        self.is_installed = False

    def install(self):
        if not self.is_installed:
            self.is_installed = True
            print(f"{self.name} installed")
        else:
            print(f"Error: {self.name} already installed")

    def uninstall(self):
        if self.is_installed:
            self.is_installed = False
            print(f"{self.name} uninstalled")
        else:
            print(f"Error: {self.name} not installed")


class InstalledPlugin(Plugin):

    def __init__(self, name, logo, repo, version):
        super().__init__(name, logo, repo, version)
        self.is_enabled = False
        self.base_stats = {}
        self.current_stats = {}

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

    def save_edits(self, edits: dict):
        print()

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

    # def get_status(self):
    #     print("fetching and returning status")

    # def get_cpu(self):
    #     cores = "command to fetch number of cpu cores"
    #     used = "command to fetch amount used, type float"
    #     total = "command to fetch total amount, type float"
    #     notes = "calulations will likely happen to convert into optimal size unit"
    #     print("Calculating and returning CPU usage (cores/used/total)")

    # def get_memory(self):
    #     used = "command to fetch amount used, type float"
    #     total = "command to fetch total amount, type float"
    #     notes = "calulations will likely happen to convert into optimal size unit"
    #     print("Calculating and returning memory usage (used/total)")

    # def get_disk(self):
    #     used = "command to fetch amount used, type float"
    #     total = "command to fetch total amount, type float"
    #     notes = "calulations will likely happen to convert into optimal size unit"
    #     print("Calculating and returning disk usage (used/total)")
