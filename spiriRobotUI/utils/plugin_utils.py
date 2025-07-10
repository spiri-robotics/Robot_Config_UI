import yaml, subprocess

from nicegui import ui
from pathlib import Path

from spiriRobotUI.utils.Plugin import (
    Plugin,
    InstalledPlugin,
    plugins,
    installed_plugins,
)

ROOT_DIR = Path(__file__).parents[2].absolute()
ICON_DIR = ROOT_DIR / "spiriRobotUI" / "icons"
REPO_DIR = ROOT_DIR / "repos"


def load_plugins():
    plugins.clear()
    for repo in REPO_DIR.iterdir():
        services_dir = repo / "services"

        if not services_dir.exists():
            print(f"No services folder found in {repo.name}. Skipping repo.")
            continue
        else:
            for folder in services_dir.iterdir():
                plugin_name = folder.name
                plugin_logo = folder / "logo.jpg"
                if not plugin_logo.exists():
                    plugin_logo = ICON_DIR / "cat_icon.jpg"
                plugin_obj = Plugin(plugin_name, plugin_logo, repo.name)
                plugins[plugin_name] = plugin_obj


def save_new_plugin(link: str | Path, check):
    repo_name = link.split("/")[-1]

    if ".git" in repo_name:
        repo_name = repo_name[:-4]
    else:
        link = f"{link}.git"

    for repo in REPO_DIR.iterdir():
        if repo_name == repo.name:
            print("Repo already cloned")
            ui.notify("Repository already added", type="negative")
            return

    command = ["git", "clone", f"{link}", f"repos/{repo_name}"]
    subprocess.run(command)

    new_repo_services = REPO_DIR / repo_name / "services"

    if not new_repo_services.exists():
        print("No services folder found in repo")
        return
    else:
        for folder in new_repo_services.iterdir():
            plugin_name = folder.name
            logo = folder / "logo.jpg"
            if not logo.exists():
                logo = ICON_DIR / "cat_icon.jpg"

            new_plug = Plugin(plugin_name, logo, repo_name)
            plugins[plugin_name] = new_plug

            if check:
                new_plug.install()

    # refresh cards (after install starts but let install run in background)
