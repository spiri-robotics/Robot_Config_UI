from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin, plugins, installed_plugins
from spiriRobotUI.utils.plugin_utils import load_plugins
from spiriRobotUI.utils.EventBus import event_bus
from spiriRobotUI.utils.styles import styles

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

_installed_repos = [
    {'name': 'Main Plugins', 'url': 'https://github.com/myorg/main-plugins', 'plugins': ['Plugin A', 'Plugin B']},
    {'name': 'Third Party', 'url': 'https://github.com/otheruser/plugins', 'plugins': ['Plugin X']}
]

def get_installed_repos():
    return _installed_repos

def add_repository(url: str):
    # Parse name or validate URL here if needed
    _installed_repos.append({'name': url.split('/')[-1], 'url': url, 'plugins': []})
    ui.notify(f"Added repo: {url}")
    ui.open('/')  # Refresh the page (or make this dynamic)

def remove_repository(repo):
    _installed_repos.remove(repo)
    ui.notify(f"Removed: {repo['name']}")
    ui.open('/')

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
    
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Available')
        two = ui.tab('Installed')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            browser_grid_ui()
        with ui.tab_panel(two):
            await installed_grid_ui()

    with ui.card().classes('w-full bg-gray-900 text-white mt-4'):
        ui.label("Installed Repositories").classes("text-lg font-bold")

        # Add repo form
        with ui.row().classes("items-center gap-4 mt-2"):
            new_repo_input = ui.input("Git Repo URL").classes("w-1/2")
            ui.button("Add Repository", on_click=lambda: add_repository(new_repo_input.value))

        ui.separator()

        # List installed repos
        for repo in get_installed_repos():
            with ui.expansion(f"{repo['name']}").classes("bg-gray-800 rounded-lg my-2"):
                ui.label(f"URL: {repo['url']}").classes("text-sm text-gray-400")

                # List plugins
                with ui.column().classes("pl-4"):
                    for plugin in repo.get('plugins', []):
                        ui.label(f"• {plugin}").classes("text-sm")

                with ui.row().classes("justify-end mt-2"):
                    ui.button("Remove", on_click=lambda r=repo: remove_repository(r)).props('color=red')
                    ui.button("Inspect", on_click=lambda r=repo: inspect_repository(r)).props('color=primary')

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