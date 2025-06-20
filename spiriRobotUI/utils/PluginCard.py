from nicegui import ui
import asyncio
from ui.ToggleButton import ToggleButton
from spiriRobotUI.utils.plugins import Plugin, InstalledPlugin
class PluginStoreCard:
    def __init__(self, plugin: Plugin):
        self.base_card_classes = ""
        self.plugin = plugin
        self.install_toggle = ToggleButton(on_label="Uninstall", off_label="Install", on_switch=lambda: self.plugin.uninstall, off_switch=lambda: self.plugin.install)
        self.install_toggle.state = plugin.is_installed

    def render(self):
        with ui.card().classes(f"{self.base_card_classes}"):
            ui.image(self.plugin.logo)
            ui.label(self.plugin.name)
            with ui.row():
                ui.label(f"Version: {self.plugin.version}")
                self.install_toggle
                
class PluginInstalledCard:
    def __init__(self, plugin: InstalledPlugin):
        self.base_card_classes = ""
        self.plugin = plugin
        self.enable_toggle = ToggleButton(on_label="Disable", off_label="Enable", on_switch=lambda:self.plugin.disable, off_switch=lambda:self.plugin.enable)
        self.enable_toggle.state = plugin.is_enabled
    
    def render(self):
        with ui.card().classes(f"{self.base_card_classes}"):
            with ui.row():
                ui.image(self.plugin.logo)
                with ui.column():
                    ui.label(self.plugin.name)
                    ui.label(self.plugin.version)
            ui.label(self.plugin.repo)
            with ui.grid(columns=2).classes("text-xl font-bold"):
                ui.label("Status")
                ui.markdown().bind_content_from(
                    self.plugin.current_stats,
                    "status",
                    backward=lambda v: f"{v}"
                )
                
                ui.markdown("CPU usage: ")
                cpu_progress = ui.linear_progress(
                    max=100, 
                    min=0, 
                    step=0.01
                    ).bind_value_from(self.plugin.current_stats['cpu'], "value")
                
                ui.markdown("Memory usage: ")
                memory_progress = ui.linear_progress(
                    max=self.plugin.base_stats['memory max'], 
                    min=0,
                    step=0.01
                    ).bind_value_from(self.plugin.current_stats['memory'])
                
                ui.markdown("Disk usage: ")
                disk_progress = ui.linear_progress(
                    max=self.plugin.base_stats['disk max'], 
                    min=0,
                    step=0.01
                    ).bind_value_from(self.plugin.current_stats['disk'])
                
                
                