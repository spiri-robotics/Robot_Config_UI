from nicegui import ui
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginStoreCard, PluginInstalledCard
from spiriRobotUI.utils.plugin_utils import plugins, installed_plugins, load_plugins

@ui.page("/")
async def main_ui():
    styles()
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
                    p = PluginStoreCard(plug)
                    p.render()
        with ui.tab_panel(two):
            if len(installed_plugins) > 0:
                with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                    for plug in installed_plugins.values():
                        p = PluginInstalledCard(plug)
                        await p.render()
            else:
                ui.label("No plugins installed yet. Please visit the 'Available' tab to install plugins.")