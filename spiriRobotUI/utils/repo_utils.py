from nicegui import ui
from git import Repo
from pathlib import Path
import shutil

from spiriRobotUI.settings import PROJECT_ROOT

installed_repos = []

for repo in (PROJECT_ROOT / "repos").iterdir():
    repo_plugins = []
    for plugin in (PROJECT_ROOT / "repos" / repo.name / "services").iterdir():
        repo_plugins.append(plugin.name)
    installed_repos.append({"name": repo.name, "plugins": repo_plugins})


@ui.refreshable
def display_repos():
    with ui.card().classes("w-full bg-gray-900 text-white mt-4"):
        ui.label("Installed Repositories").classes("text-lg font-bold")

        # Add repo form
        with ui.row().classes("items-center gap-4 mt-2"):
            new_repo_input = ui.input("Git Repo URL").classes("w-1/2")
            ui.button(
                "Add Repository",
                on_click=lambda: add_repository(new_repo_input.value),
                color="secondary",
            )

        ui.separator()

        # List installed repos
        for repo in installed_repos:
            with ui.expansion(f"{repo['name']}").classes("bg-gray-800 rounded-lg my-2"):

                # List plugins
                with ui.column().classes("pl-4"):
                    for plugin in repo.get("plugins", []):
                        ui.label(f"• {plugin}").classes("text-sm")

                ui.button("Remove", on_click=lambda r=repo: remove_repository(r)).props(
                    "color=red"
                )


def add_repository(url: str):
    repos_dir = PROJECT_ROOT / "repos"
    repos_dir.mkdir(exist_ok=True)

    # Extract folder name from repo URL (e.g., "my-plugins")
    repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
    clone_path = repos_dir / repo_name

    if clone_path.exists():
        ui.notify(f"Repository '{repo_name}' already exists.", type="warning")
        return

    try:
        Repo.clone_from(url, clone_path)
        if clone_path.exists():
            repo_plugins = []
            for plugin in (PROJECT_ROOT / "repos" / repo.name / "services").iterdir():
                repo_plugins.append(plugin.name)
            installed_repos.append({"name": repo_name, "plugins": repo_plugins})
            ui.notify(f"Cloned {repo_name} into /repos")
            display_repos.refresh()
        else:
            ui.notify("Clone Failed.")
    except Exception as e:
        ui.notify(f"Error cloning repo: {e}", type="negative")


def remove_repository(repo):
    if repo in installed_repos:
        installed_repos.remove(repo)

    # Delete directory from repos/
    repo_path = Path(PROJECT_ROOT / "repos" / repo["name"])
    try:
        if repo_path.exists() and repo_path.is_dir():
            shutil.rmtree(repo_path)
            ui.notify(f"Deleted repository: {repo['name']}")
            display_repos.refresh()
        else:
            ui.notify(f"Repo directory not found: {repo_path}", type="warning")
    except Exception as e:
        ui.notify(f"Error deleting repo: {e}", type="negative")
