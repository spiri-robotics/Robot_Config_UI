from nicegui import ui, Client

from spiriRobotUI.components.PluginDialog import PluginDialog
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin, plugins, installed_plugins
from spiriRobotUI.utils.styles import style_vars
from spiriRobotUI.utils.system_utils import cores, memory, disk 


class PluginBrowserCard:
    def __init__(self, plugin: Plugin):
        self.base_card_classes = f"flex-col shadow-[{style_vars['flex-shadow']}]"
        self.plugin_dialog = PluginDialog(plugin)
        self.plugin = plugin
        self.install_toggle = None

    @ui.refreshable
    def render(self):
        with ui.card().tight().classes(
            f"w-56 mb-2 transition transform hover:scale-105 {self.base_card_classes}"
        ):
            with ui.card_section().classes('w-full justify-center'):
                card_image = ui.image(self.plugin.logo).classes(
                    "w-full cursor-pointer rounded self-center"
                )
                
            ui.separator()
            
            with ui.card_section().classes("w-full"):
                ui.label(self.plugin.name.title()).classes("text-lg font-medium pb-4")
                self.install_toggle = ToggleButton(
                    on_label="Uninstall",
                    off_label="Install",
                    on_switch=lambda: self.plugin.uninstall(),
                    off_switch=lambda: self.plugin.install(),
                    state=self.plugin.is_installed,
                    on_color="warning",
                    off_color="secondary",
                ).classes("w-full")

        def open_dialog():
            self.plugin_dialog.generate_dialog()
            self.plugin_dialog.dialog.open()

        card_image.on("click", open_dialog)


class PluginInstalledCard:
    def __init__(self, plugin: InstalledPlugin):
        self.base_card_classes = ""
        self.plugin = plugin

    @ui.refreshable
    async def render(self):
        self.plugin.get_current_stats()
        
        with ui.card().tight().classes(f"w-80"):
            with ui.card_section().classes('w-full'):
                with ui.row().classes("justify-between w-full"):
                    ui.image(self.plugin.logo).classes("w-24 h-24 rounded")
                    self.enable_toggle = ToggleButton(
                        on_label="Disable",
                        off_label="Enable and Start",
                        on_switch=self.plugin.stop,
                        off_switch=self.plugin.run,
                        state=self.plugin.is_running,
                        on_color="warning",
                        off_color="secondary",
                    ).classes("w-32 h-24")
            
            with ui.card_section().classes('w-full'):
                ui.label(self.plugin.name.title()).classes("text-xl font-medium")
                ui.label(self.plugin.repo).classes('text-base font-light')
            
            if self.plugin.is_running:
                ui.separator()
                
                with ui.card_section().classes('w-full'):
                    with ui.grid(columns=2).classes("w-full text-lg"):
                        ui.label("Status:").classes('font-medium')
                        ui.label().classes('text-lg font-light').bind_text_from(
                            self.plugin.current_stats, "status", backward=lambda v: f"{v}"
                        )
                        
                ui.separator()
                
                with ui.card_section().classes('w-full'):
                    with ui.grid(columns=2).classes("w-full text-base font-light items-center"):
                        ui.label("CPU usage: ")
                        ui.linear_progress().bind_value_from(lambda: self.plugin.current_stats["cpu"])
                        
                        ui.label("Memory usage: ")
                        ui.linear_progress().bind_value_from(
                            lambda: self.plugin.current_stats["memory"] / self.plugin.current_stats["memory_limit"]
                        )
                        
                        ui.label("Disk usage: ")
                        ui.linear_progress().bind_value_from(
                            lambda: self.plugin.current_stats["disk"] / disk
                        )
                    
                ui.separator()
                
                with ui.card_section().classes('w-full'):
                    with ui.grid(rows=2, columns=6):
                        ui.button("UNINSTALL", color='warning', on_click=lambda: self.uninstall_plugin()).classes('col-end-[span_3]')
                        ui.button("VIEW LOGS", color='secondary', on_click=lambda: self.get_logs()).classes('col-end-[span_3]')
                        ui.button("EDIT", color='secondary', on_click=lambda: self.edit_env()).classes('col-end-[span_2]')
                        ui.button("RESTART", color='secondary', on_click=lambda: self.restart_plugin()).classes('col-end-[span_2]')
                        ui.button("UPDATE", color='secondary', on_click=lambda: self.plugin.update()).classes('col-end-[span_2]')
                    
    def uninstall_plugin(self):
        self.plugin.uninstall()

    def get_logs(self):
        logs = self.plugin.get_logs()
        with ui.dialog() as dialog:
            with ui.card():
                ui.label("Plugin Logs").classes("text-lg font-bold")
                ui.textarea(logs).classes("w-full h-64").props("readonly")
                with ui.row().classes("justify-end"):
                    ui.button(
                        "",
                        icon="download",
                        on_click=lambda: ui.download.file("logs.txt"),
                        color="secondary",
                    )
                    ui.button("Close", color="secondary", on_click=dialog.close)
        dialog.classes("w-3/4 h-3/4")
        dialog.props("scrollable")
        dialog.open()

    def edit_env(self):
        env = self.plugin.get_env()
        with ui.dialog() as dialog:
            with ui.card().classes("w-3/4 h-3/4"):
                ui.label("Edit Environment Variables").classes("text-lg font-bold")
                code = ui.codemirror(env, language="json").classes("w-full h-64")
                code.props(
                    'mode="application/json" line-numbers theme="default" readonly=false tab-size=2 auto-close-brackets match-brackets line-wrapping'
                )
                with ui.row().classes("justify-end"):
                    ui.button(
                        "Save",
                        color="secondary",
                        on_click=lambda: self.plugin.set_env(code.value),
                    )
                    ui.button("Close", color="secondary", on_click=dialog.close)
        dialog.open()

    async def restart_plugin(self):
        await self.plugin.stop()
        print(self.plugin.is_running)
        await self.plugin.run()
