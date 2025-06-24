from pathlib import Path


class Plugin:
    """Base class for all plugins"""

    def __init__(
            self, 
            name: str, 
            logo: str | Path, 
            repo: str, 
            versions: list
        ):

        self.name = name
        self.logo = logo
        self.url = ""
        self.repo = repo
        self.versions = versions

        self.is_installed = False
        self.readme_contents = self.get_readme_contents()

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

    def get_readme_contents(self):
        path = f"repos/{self.repo}/services/{self.name}/README.md"
        if Path(path).exists():
            with open(path, "r") as f:
                readme_contents = f.read()
            return readme_contents
        else:
            return ""


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
