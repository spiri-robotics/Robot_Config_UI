from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.EventBus import event_bus
from spiriRobotUI.utils.Plugin import plugins, installed_plugins
from spiriRobotUI.utils.plugins_page_utils import (
    browser_cards, installed_cards, 
    register_plugins, register_installed, 
    create_browser_cards, update_installed_cards, 
    browser_grid_ui, installed_grid_ui
)
from spiriRobotUI.utils.repo_utils import display_repos, add_repository
from spiriRobotUI.utils.styles import styles


@ui.page("/")
async def main_ui():
    await styles()
    sidebar()

    with ui.row(align_items='end'):
        header()
        ui.markdown("## Plug-in Coordinator")
    with ui.row(align_items='end').classes('w-full justify-between'):
        ui.label("Your favourite plugins, now all in one place.").classes('text-xl font-light')
        ui.button(
            "Add Repository",
            on_click=add_repository,
            color="secondary",
        )

    ui.separator()

    register_plugins()
    register_installed()
    
    create_browser_cards()
    update_installed_cards()
    
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Available')
        two = ui.tab('Installed')
        three = ui.tab('Repositories')
    with ui.tab_panels(tabs, value=one).classes('w-full bg-transparent').props('animated=false'):
        with ui.tab_panel(one):
            browser_grid_ui()
        with ui.tab_panel(two):
            await installed_grid_ui()
        with ui.tab_panel(three):
            display_repos()


def on_plugin_installed(plugin_name: str):
    global installed_cards
    plugin = installed_plugins[plugin_name]
    installed_cards[plugin.name] = PluginInstalledCard(plugin)
    browser_cards[plugin_name].render.refresh()
    installed_grid_ui.refresh()


def on_plugin_uninstalled(plugin_name: str):
    global installed_cards
    if plugin_name in installed_cards.keys():
        del installed_cards[plugin_name]
    installed_grid_ui.refresh()
    plugins[plugin_name].is_installed = False
    browser_cards[plugin_name].render.refresh()


def on_plugin_run(plugin_name: str):
    global installed_cards
    installed_cards[plugin_name].render.refresh()


event_bus.on("plugin_installed", on_plugin_installed)
event_bus.on("plugin_uninstalled", on_plugin_uninstalled)

event_bus.on("plugin_run", on_plugin_run)
