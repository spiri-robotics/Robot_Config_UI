from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin, plugins, installed_plugins
from spiriRobotUI.utils.plugin_utils import load_plugins
from spiriRobotUI.utils.styles import styles

def add_new_plugin_card(plugin: Plugin):
    """Add a new plugin card to the UI."""
    new_card = PluginBrowserCard(plugin)
    new_card.render()

def add_installed_card(plugin: InstalledPlugin):
    new_card = PluginInstalledCard(plugin)
    new_card.render()

@ui.page("/")
async def main_ui():
    await styles()
    sidebar()
    header()
    ui.markdown("## Plug-in Coordinator")
    ui.label("Your favourite plugins, now all in one place.")

    ui.separator()

    load_plugins()

    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Available')
        two = ui.tab('Installed')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                for plug in plugins.values():
                    p = PluginBrowserCard(plug)
                    p.render()
        with ui.tab_panel(two):
            if len(installed_plugins) == 0:
                ui.label(
                    "No plugins installed yet. Please visit the 'Available' tab to install plugins."
                )
            else:
                with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                    for plugin_name in plugins:
                        add_installed_card(installed_plugins[plugin_name])
