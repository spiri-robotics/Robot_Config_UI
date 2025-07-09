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
    installed_grid_ui.refresh()

def on_plugin_uninstalled(plugin_name: str):
    del installed_cards[plugin_name]
    installed_grid_ui.refresh()
    

event_bus.on("plugin_installed", on_plugin_installed)
event_bus.on("plugin_uninstalled", on_plugin_uninstalled)