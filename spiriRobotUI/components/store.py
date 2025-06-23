from nicegui import ui
from spiriRobotUI.classes.PluginCard import PluginStoreCard, PluginInstalledCard
from spiriRobotUI.classes.ToggleButton import ToggleButton
from spiriRobotUI.utils.plugin_utils import plugins, load_plugins

plugin_cards = {}

async def home():
    ui.label("Plugin Coordinator").classes('mt-0 text-4xl font-light')
    ui.label("Your favourite plugins, now all in one place.")
    ui.separator()

    load_plugins()

    with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
        for name, plug in plugins.items():
            new_plug = PluginStoreCard(plug)
            plugin_cards[name] = new_plug
            await new_plug.render()