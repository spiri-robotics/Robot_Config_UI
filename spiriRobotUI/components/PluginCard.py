from nicegui import ui

from spiriRobotUI.components.PluginDialog import PluginDialog
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin, plugins, installed_plugins
from spiriRobotUI.utils.styles import DARK_MODE


class PluginBrowserCard:
    def __init__(self, plugin: Plugin):
        self.base_card_classes = "w-56 h-64 flex-col justify-between"
        self.plugin_dialog = PluginDialog(plugin)
        self.plugin = plugin
        self.install_toggle = None

    def render(self):
        browser_card = ui.card().classes(
            f"transition transform hover:scale-105 hover:border-blue-500 {self.base_card_classes}"
        )
        if DARK_MODE:
            browser_card.classes(f"dark-card")
            
        with browser_card:
            card_image = ui.image(self.plugin.logo).classes(
                "w-full h-48 object-cover cursor-pointer"
            )
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(self.plugin.name.replace('-', ' ').title()).classes("text-xl font-normal")
                self.install_toggle = ToggleButton(
                    on_label="Install",
                    off_label="Uninstall",
                    on_switch=lambda: self.plugin.install(),
                    off_switch=lambda: self.plugin.uninstall(),
                    state=not self.plugin.is_installed,
                    on_color="secondary",
                    off_color="warning",
                ).classes("w-1/2")

        def open_dialog():
            self.plugin_dialog.generate_dialog()
            self.plugin_dialog.dialog.open()

        card_image.on("click", open_dialog)

class PluginInstalledCard:
    def __init__(self, plugin: InstalledPlugin):
        self.base_card_classes = ""
        self.plugin = plugin

    def render(self):
        self.plugin.get_current_stats()
        self.plugin.get_base_stats()
        installed_card = ui.card().classes(f"{self.base_card_classes}")
        if DARK_MODE:
            installed_card.classes(f"dark-card")
        with installed_card:
            with ui.row().classes("justify-between w-full"):
                ui.image(self.plugin.logo).classes("w-24 h-24")
                self.enable_toggle = ToggleButton(
                    on_label="Disable",
                    off_label="Enable and Start",
                    on_switch=lambda: self.plugin.stop,
                    off_switch=lambda: self.plugin.run,
                    state=self.plugin.is_running,
                    on_color="secondary",
                    off_color="warning",
                ).classes("w-28 h-24")
            ui.separator()
            with ui.row().classes("justify-between w-full"):
                ui.label(self.plugin.name.replace('-', ' ').capitalize()).classes("text-lg font-bold")
            ui.separator()
            ui.label(self.plugin.repo)
            ui.separator()
            with ui.grid(columns=2).classes("text-xl font-bold"):
                ui.label("Status")
                ui.markdown().bind_content_from(
                    self.plugin.current_stats, "status", backward=lambda v: f"{v}"
                )

                ui.markdown("CPU usage: ")
                cpu_progress = ui.linear_progress().bind_value_from(
                    self.plugin.current_stats["cpu"]
                )

                ui.markdown("Memory usage: ")
                memory_progress = ui.linear_progress().bind_value_from(
                    self.plugin.current_stats["memory"]
                    / self.plugin.base_stats["memory"]
                )

                ui.markdown("Disk usage: ")
                disk_progress = ui.linear_progress().bind_value_from(
                    self.plugin.current_stats["disk"] / self.plugin.base_stats["disk"]
                )
