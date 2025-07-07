import asyncio

from nicegui import ui

from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.Plugin import Plugin
from spiriRobotUI.utils.styles import DARK_MODE


class PluginDialog:
    def __init__(self, plugin: Plugin):
        self.plugin = plugin
        self.dialog = None

    def generate_dialog(self):
        self.dialog = ui.dialog()
        with self.dialog:
            outer_card = ui.card().classes("items-left h-1/2 w-full")
            with outer_card:
                with ui.row().classes("w-full justify-between items-center"):
                    ui.image(self.plugin.logo).classes("w-24 h-24 rounded")
                    name_card = ui.card().classes(
                        "w-3/4 h-24 items-center justify-center"
                    )
                    with name_card:
                        with ui.row().classes("w-full justify-between"):
                            ui.label(self.plugin.name.replace('-', ' ').title()).classes("text-3xl font-light")
                            self.install_toggle = ToggleButton(
                                on_label="Install",
                                off_label="Uninstall",
                                on_switch=lambda: self.plugin.install(),
                                off_switch=lambda: self.plugin.uninstall(),
                                state=not self.plugin.is_installed,
                                on_color="secondary",
                                off_color="warning",
                            )
                with ui.column().classes("w-full"):
                    ui.markdown(self.plugin.readme_contents)

        if DARK_MODE:
            name_card.classes("dark-card")
            outer_card.classes("dark-card")
