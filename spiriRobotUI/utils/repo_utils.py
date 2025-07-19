import shutil

from nicegui import ui
from git import Repo
from pathlib import Path

from spiriRobotUI.utils.styles import style_vars
from spiriRobotUI.settings import PROJECT_ROOT
from spiriRobotUI.utils.plugins_page_utils import register_plugins, create_browser_cards, browser_grid_ui

installed_repos = []

for repo in (PROJECT_ROOT / "repos").iterdir():
    repo_plugins = []
    for plugin in (repo / "services").iterdir():
        repo_plugins.append(plugin.name)
    installed_repos.append({"name": repo.name, "plugins": repo_plugins})


@ui.refreshable
def display_repos():
    # List installed repos
    if len(installed_repos) > 0:
        with ui.grid(columns=3):
            for repo in installed_repos:
                with ui.card().classes(f'shadow-[{style_vars["flex-shadow"]}]'):
                    ui.label(f"{repo['name']}").classes('text-lg font-medium')
                    # List plugins
                    with ui.column().classes("pl-4 pb-2"):
                        for plugin in repo.get("plugins", []):
                            ui.label(f"• {plugin}").classes("text-base font-light")

                    ui.button("Remove", on_click=lambda r=repo: remove_repository(r), color='negative')
            add_repo =  ui.card().classes(f'items-center transition transform hover:scale-[1.03] shadow-[{style_vars["flex-shadow"]}]')
            with add_repo:
                ui.label("Add a Repository").classes('text-lg font-medium')
                ui.image("spiriRobotUI/icons/add_repo.svg")
            add_repo.on("click", add_repository)
            
    else:
        ui.label("No Repositories Added").classes('text-base font-light')

def repo_dialog() -> ui.dialog:
    with ui.dialog() as d, ui.card().classes('w-1/4'):
        ui.label('Add A Repository').classes('text-xl font-medium')
        new_repo_input = ui.input('Repository URL').classes('w-full')
        ui.button(
            'Add',
            on_click=lambda: d.submit(new_repo_input.value),
            color='secondary'
        ).classes('self-center')
    return d

async def add_repository():
    dialog = repo_dialog()
    url = await dialog
    
    if url is not None:
        repos_dir = PROJECT_ROOT / "repos"
        repos_dir.mkdir(exist_ok=True)

        # Extract folder name from repo URL (e.g., "my-plugins")
        repo_name = str(url).rstrip("/").split("/")[-1].replace(".git", "")
        clone_path = repos_dir / repo_name

        if clone_path.exists():
            ui.notify(f"Repository '{repo_name}' already exists.", type="warning")
            return

        try:
            Repo.clone_from(url, clone_path)
            if clone_path.exists():
                repo_plugins = []
                for plugin in (clone_path / "services").iterdir():
                    repo_plugins.append(plugin.name)
                installed_repos.append({"name": repo_name, "plugins": repo_plugins})
                ui.notify(f"Cloned {repo_name} into /repos")
                display_repos.refresh()
                register_plugins()
                create_browser_cards()
                browser_grid_ui.refresh()
                
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
            register_plugins()
            create_browser_cards()
            browser_grid_ui.refresh()
        else:
            ui.notify(f"Repo directory not found: {repo_path}", type="warning")
    except Exception as e:
        ui.notify(f"Error deleting repo: {e}", type="negative")
