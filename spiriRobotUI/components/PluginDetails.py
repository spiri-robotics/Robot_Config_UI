import asyncio
from nicegui import ui
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.components.PluginCard import PluginStoreCard, PluginInstalledCard
from spiriRobotUI.utils.plugins import Plugin

class PluginDialog:
    def __init__(self, plugin: Plugin):
        self.plugin = plugin
    
    def render(self):
        with ui.dialog() as plugin_dialog, ui.card().classes('items-center'):
            with ui.row():
                ui.image(self.plugin.logo).classes("w-32 h-32")
                with ui.column().classes("items-start"):
                    ui.label(self.plugin.name).classes("text-xl font-bold")
                    ui.label("will be description of app").classes("text-sm text-gray-400")
                    ui.label("What architectures it can run on e.g. ARM, AMD64").classes("text-sm font-bold text-gray-300")
            with ui.row().classes("w-full"):
                version = ui.select(self.plugin.versions, value=self.plugin.versions[-1]).classes('text-base w-4/5')
                install_toggle = ToggleButton(
                    on_label="Uninstall",
                    off_label="Install",
                    on_switch=lambda: self.plugin.uninstall(),
                    off_switch=lambda: self.plugin.install(),
                )