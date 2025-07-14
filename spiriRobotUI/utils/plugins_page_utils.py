from nicegui import ui

from spiriRobotUI.utils.Plugin import plugins, installed_plugins, Plugin, InstalledPlugin, REPOS, SERVICES
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard

browser_cards = {}
installed_cards = {}

def register_plugins():
    # Scan the REPOS directory and register all plugins
    plugins.clear()
    for repo in REPOS.iterdir():
        for plugin in (repo / "services").iterdir():
            logo = plugin / "logo.jpg"
            if not logo.exists():
                logo = "spiriRobotUI/icons/spiri_drone_ui_logo.svg"
            plugins[plugin.name] = Plugin(plugin.name, str(logo), repo.name, plugin.name)
            
def register_installed():
    # Scan the SERVICES directory and register installed plugins.
    installed_plugins.clear()
    for service_dir in SERVICES.iterdir():
        if service_dir.is_dir():
            for plugin in plugins.values():
                if (
                    service_dir.name == plugin.folder_name
                    and plugin.name not in installed_plugins
                ):
                    plugin.is_installed = True
                    installed_plugins[plugin.name] = InstalledPlugin(
                        plugin.name, plugin.logo, plugin.repo, plugin.folder_name
                    )
                
def create_browser_cards():
    browser_cards.clear()
    for plugin in plugins.values():
        browser_cards[plugin.name] = PluginBrowserCard(plugin)


def update_installed_cards():
    for plugin in installed_plugins.values():
        if plugin.name not in installed_cards.keys():
            installed_cards[plugin.name] = PluginInstalledCard(plugin)
            
@ui.refreshable   
def browser_grid_ui():
    if len(browser_cards) > 0:
        with ui.row(align_items='stretch').classes(f"w-full"):
            for card in browser_cards.values():
                card.render()
    else:
        ui.label('No plugins available. Please add a repository to view plugins.').classes('text-base font-light')


@ui.refreshable
async def installed_grid_ui():
    if len(installed_plugins) == 0:
        ui.label(
            "No plugins installed yet. Please visit the 'Available' tab to install plugins."
        ).classes('text-base font-light')
    else:
        with ui.row(align_items='stretch').classes("w-full"):
            for card in installed_cards.values():
                await card.render()