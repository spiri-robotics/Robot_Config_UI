from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin, plugins, installed_plugins
from spiriRobotUI.utils.plugin_utils import load_plugins
from spiriRobotUI.utils.EventBus import event_bus
from spiriRobotUI.utils.styles import styles, style_vars


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
    ui.label("Your favourite plugins, now all in one place.").classes('text-lg font-light')

    ui.separator()

    load_plugins()
    create_browser_cards()
    update_installed_cards()
    
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Available')
        two = ui.tab('Installed')
    with ui.tab_panels(tabs, value=two).classes('w-full bg-transparent').props('animated=false'):
        with ui.tab_panel(one):
            browser_grid_ui()
        with ui.tab_panel(two):
            await installed_grid_ui()
            a = InstalledPlugin('test', 'spiriRobotUI/icons/spiri_drone_ui_logo.svg', 'robot-config-test-repo', 'webapp-example')
            b = PluginInstalledCard(a)
            await b.render()

@ui.refreshable   
def browser_grid_ui():
    with ui.row(align_items='stretch').classes(f"w-full"):
        for card in browser_cards.values():
            card.render()

@ui.refreshable
async def installed_grid_ui():
    if len(installed_plugins) == 0:
        ui.label(
            "No plugins installed yet. Please visit the 'Available' tab to install plugins."
        )
    else:
        with ui.row(align_items='stretch').classes("w-full"):
            for card in installed_cards.values():
                await card.render()

def on_plugin_installed(plugin_name: str):
    plugin = installed_plugins[plugin_name]
    installed_cards[plugin.name] = PluginInstalledCard(plugin)
    browser_cards[plugin_name].render.refresh()
    installed_grid_ui.refresh()

def on_plugin_uninstalled(plugin_name: str):
    del installed_cards[plugin_name]
    browser_cards[plugin_name].render.refresh()
    installed_grid_ui.refresh()
    

event_bus.on("plugin_installed", on_plugin_installed)
event_bus.on("plugin_uninstalled", on_plugin_uninstalled)