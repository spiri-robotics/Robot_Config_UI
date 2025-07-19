from nicegui import app, ui

from spiriRobotUI.utils.Plugin import plugins, installed_plugins, Plugin, InstalledPlugin, REPOS, SERVICES
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard

browser_cards = {}
installed_cards = {}

def register_plugins():
    # Scan the REPOS directory and register all plugins
    plugins.clear()
    for repo in REPOS.iterdir():
        plugins[repo.name] = {}
        for plugin in (repo / "services").iterdir():
            logo = plugin / "logo.jpg"
            if not logo.exists():
                logo = "spiriRobotUI/icons/placeholder_logo.png"
            plugins[repo.name][plugin.name] = Plugin(plugin.name, str(logo), repo.name, plugin.name)
            
def register_installed():
    # Scan the SERVICES directory and register installed plugins.
    installed_plugins.clear()
    for service_dir in SERVICES.iterdir():
        if service_dir.is_dir():
            has_repo = False
            for repo in plugins.keys():
                for plugin in plugins[repo].values():
                    if (
                        service_dir.name == plugin.folder_name
                        and plugin.name not in installed_plugins
                    ):
                        plugin.is_installed = True
                        has_repo = True
                        installed_plugins[plugin.name] = InstalledPlugin(
                            plugin.name, plugin.logo, plugin.repo, plugin.folder_name
                        )
                    
            if not has_repo:
                logo = service_dir / "logo.jpg"
                if not logo.exists():
                    logo = "spiriRobotUI/icons/cat_icon.jpg"
                installed_plugins[service_dir.name] = InstalledPlugin(
                    service_dir.name, logo, None, service_dir.name
                )
                installed_plugins[service_dir.name].is_installed = True
                
def create_browser_cards():
    browser_cards.clear()
    for repo in plugins.keys():
        browser_cards[repo] = {}
        for plugin in plugins[repo].values():
            browser_cards[repo][plugin.name] = PluginBrowserCard(plugin)


def update_installed_cards():
    for plugin in installed_plugins.values():
        if plugin.name not in installed_cards.keys():
            installed_cards[plugin.name] = PluginInstalledCard(plugin)
            
@ui.refreshable   
def browser_grid_ui():
    if len(browser_cards) > 0:
        for repo in browser_cards.keys():
            ui.label(f'{repo}:').classes('text-lg font-medium')
            with ui.row(align_items='stretch').classes(f"w-full"):
                for card in browser_cards[repo].values():
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
                
@app.on_shutdown
def cleanup_plugin_polling():
    for card in installed_cards.values():
        if card.polling_task and not card.polling_task.done():
            card.polling_task.cancel()
