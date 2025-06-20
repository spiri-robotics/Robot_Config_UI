import asyncio

from nicegui import ui

from spiriRobotUI.components.PluginDetails import PluginDialog
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.plugins import InstalledPlugin, Plugin


class PluginStoreCard:
    def __init__(self, plugin: Plugin):
        self.base_card_classes = "w-56 h-64 flex-col justify-between"
        self.plugin_dialog = PluginDialog(plugin)
        self.plugin = plugin

    def render(self):
        store_card = ui.card().classes(f"{self.base_card_classes} cursor-pointer")
        with store_card:
            ui.image(self.plugin.logo).classes("w-full h-32 object-cover")
            ui.label(self.plugin.name).classes("text-lg font-bold")
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(f"Version: {self.plugin.versions[0]}")
                install_toggle = ToggleButton(
                    on_label="Uninstall",
                    off_label="Install",
                    on_switch=lambda: self.plugin.uninstall(),
                    off_switch=lambda: self.plugin.install(),
                )
            install_toggle.state = self.plugin.is_installed

        def open_dialog():
            self.plugin_dialog.generate_dialog()
            self.plugin_dialog.dialog.open()

        store_card.on("click", open_dialog)


class PluginInstalledCard:
    def __init__(self, plugin: InstalledPlugin):
        self.base_card_classes = ""
        self.plugin = plugin
        self.enable_toggle = ToggleButton(
            on_label="Disable",
            off_label="Enable",
            on_switch=lambda: self.plugin.disable,
            off_switch=lambda: self.plugin.enable,
        )
        self.enable_toggle.state = plugin.is_enabled

    def render(self):
        with ui.card().classes(f"{self.base_card_classes}"):
            with ui.row():
                ui.image(self.plugin.logo)
                with ui.column():
                    ui.label(self.plugin.name)
                    ui.label(self.plugin.versions[0])
            ui.label(self.plugin.repo)
            with ui.grid(columns=2).classes("text-xl font-bold"):
                ui.label("Status")
                ui.markdown().bind_content_from(
                    self.plugin.current_stats, "status", backward=lambda v: f"{v}"
                )

                ui.markdown("CPU usage: ")
                cpu_progress = ui.linear_progress(
                    max=100, min=0, step=0.01
                ).bind_value_from(self.plugin.current_stats["cpu"], "value")

                ui.markdown("Memory usage: ")
                memory_progress = ui.linear_progress(
                    max=self.plugin.base_stats["memory max"], min=0, step=0.01
                ).bind_value_from(self.plugin.current_stats["memory"])

                ui.markdown("Disk usage: ")
                disk_progress = ui.linear_progress(
                    max=self.plugin.base_stats["disk max"], min=0, step=0.01
                ).bind_value_from(self.plugin.current_stats["disk"])
