from nicegui import ui
from git import Repo
from pathlib import Path
import shutil

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.Plugin import plugins, installed_plugins
from spiriRobotUI.utils.plugin_utils import load_plugins
from spiriRobotUI.utils.EventBus import event_bus
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.settings import PROJECT_ROOT

browser_cards = {}
installed_cards = {}


def create_browser_cards():
    for plugin in plugins.values():
        if plugin.name not in browser_cards.keys():
            browser_cards[plugin.name] = PluginBrowserCard(plugin)


def update_installed_cards():
    for plugin in installed_plugins.values():
        if plugin.name not in installed_cards.keys():
            installed_cards[plugin.name] = PluginInstalledCard(plugin)


installed_repos = []

for repo in (PROJECT_ROOT / "repos").iterdir():
    repo_plugins = []
    for plugin in (PROJECT_ROOT / "repos" / repo.name / "services").iterdir():
        repo_plugins.append(plugin.name)
    installed_repos.append({"name": repo, "plugins": repo_plugins})


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
        ui.notify(f"Cloned {repo_name} into /repos")

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
        else:
            ui.notify(f"Repo directory not found: {repo_path}", type="warning")
    except Exception as e:
        ui.notify(f"Error deleting repo: {e}", type="negative")


def inspect_repository(repo):
    ui.notify(f"Inspecting: {repo['name']}")
    # You can open a new page or modal here


@ui.page("/")
async def main_ui():
    await styles()
    sidebar()
    header()
    ui.markdown("## Plug-in Coordinator")
    ui.label("Your favourite plugins, now all in one place.")

    ui.separator()

    load_plugins()
    create_browser_cards()
    update_installed_cards()

    with ui.tabs().classes("w-full") as tabs:
        one = ui.tab("Available")
        two = ui.tab("Installed")
    with ui.tab_panels(tabs, value=one).classes("w-full"):
        with ui.tab_panel(one):
            browser_grid_ui()
        with ui.tab_panel(two):
            await installed_grid_ui()

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

                with ui.row().classes("justify-end mt-2"):
                    ui.button(
                        "Remove", on_click=lambda r=repo: remove_repository(r)
                    ).props("color=red")
                    ui.button(
                        "Inspect", on_click=lambda r=repo: inspect_repository(r)
                    ).props("color=secondary")


@ui.refreshable
def browser_grid_ui():
    with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
        for card in browser_cards.values():
            card.render()


@ui.refreshable
async def installed_grid_ui():
    if len(installed_plugins) == 0:
        ui.label(
            "No plugins installed yet. Please visit the 'Available' tab to install plugins."
        )
    else:
        with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
            for card in installed_cards.values():
                await card.render()


def on_plugin_installed(plugin_name: str):
    plugin = installed_plugins[plugin_name]
    installed_cards[plugin.name] = PluginInstalledCard(plugin)
    browser_cards[plugin_name].render.refresh()
    installed_grid_ui.refresh()


def on_plugin_uninstalled(plugin_name: str):
    if plugin_name in installed_cards.keys():
        del installed_cards[plugin_name]
    browser_cards[plugin_name].render.refresh()
    installed_grid_ui.refresh()


event_bus.on("plugin_installed", on_plugin_installed)
event_bus.on("plugin_uninstalled", on_plugin_uninstalled)
