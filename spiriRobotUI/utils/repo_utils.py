import shutil

from nicegui import ui
from git import Repo
from pathlib import Path

from spiriRobotUI.utils.styles import style_vars
from spiriRobotUI.settings import PROJECT_ROOT
from spiriRobotUI.utils.plugins_page_utils import register_plugins, create_browser_cards, browser_grid_ui

installed_repos = []

for repo in (PROJECT_ROOT / "repos").iterdir():
    installed_repos.append(repo.name)


@ui.refreshable
def display_repos():
    # List installed repos
    with ui.grid(columns=3).classes('gap-4'):
        for repo in installed_repos:
            with ui.card().classes(
                'aspect-square w-full flex flex-col justify-between items-center '
                f'shadow-[{style_vars["flex-shadow"]}]'
            ):
                ui.label(f"{repo}").classes('text-lg font-medium')
                ui.button("Remove", on_click=lambda r=repo: remove_repository(r), color='negative').classes('w-full')

        # Add repo card (direct with block)
        with ui.card().classes(
            'aspect-square w-full flex flex-col justify-center items-center cursor-pointer '
            f'transition transform hover:scale-[1.03] shadow-[{style_vars["flex-shadow"]}]'
        ).on('click', add_repository):
            ui.label("Add a Repository").classes('text-lg font-medium')
            ui.image("spiriRobotUI/icons/add_repo.svg").classes('w-12 h-12')


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
                installed_repos.append(repo_name)
                ui.notify(f"Cloned {repo_name} into /repos")
                display_repos.refresh()
                register_plugins()
                create_browser_cards()
                browser_grid_ui.refresh()
                
            else:
                ui.notify("Clone Failed.")
        except Exception as e:
            ui.notify(f"Error cloning repo: {e}", type="negative")


def remove_repository(repo_name: str):
    if repo_name in installed_repos:
        installed_repos.pop(installed_repos.index(repo_name))

    # Delete directory from repos/
    repo_path = Path(PROJECT_ROOT / "repos" / repo_name)
    try:
        if repo_path.exists() and repo_path.is_dir():
            shutil.rmtree(repo_path)
            ui.notify(f"Deleted repository: {repo_name}")
            display_repos.refresh()
            register_plugins()
            create_browser_cards()
            browser_grid_ui.refresh()
        else:
            ui.notify(f"Repo directory not found: {repo_path}", type="warning")
    except Exception as e:
        ui.notify(f"Error deleting repo: {e}", type="negative")
