from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginStoreCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.plugins import Plugin

plugins = {
    "plugin1": Plugin(
        "plugin1",
        "spiriRobotUI/icons/cat_icon.jpg",
        "https://example.com/plugin1",
        ["1", "2"],
    )
}

plugin_cards = {}


def add_new_plugin_card(plugin: Plugin):
    """Add a new plugin card to the UI."""
    new_card = PluginStoreCard(plugin)
    new_card.render()
    plugin_cards[plugin.name] = new_card


@ui.page("/")
async def main_ui():
    sidebar()
    header()
    ui.markdown("## Plug-in Coordinator")
    ui.label("Your favourite plugins, now all in one place.")

    ui.separator()

    with ui.tabs().classes("w-full") as tabs:
        one = ui.tab("Available")
        two = ui.tab("Installed")
    with ui.tab_panels(tabs, value=one).classes("w-full"):
        with ui.tab_panel(one):
            with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                for plugin_name in plugins:
                    add_new_plugin_card(plugins[plugin_name])
        with ui.tab_panel(two):
            ui.label(
                "No plugins installed yet. Please visit the 'Available' tab to install plugins."
            )
            with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                for plugin_name in plugins:
                    add_new_plugin_card(plugins[plugin_name])
