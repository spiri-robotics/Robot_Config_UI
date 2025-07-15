from nicegui import ui
import asyncio
from spiriRobotUI.components.PluginDialog import PluginDialog
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin
from spiriRobotUI.utils.EventBus import event_bus
from spiriRobotUI.utils.styles import DARK_MODE
from spiriRobotUI.utils.system_utils import disk


class PluginBrowserCard:
    def __init__(self, plugin: Plugin):
        self.base_card_classes = "w-56 h-64 flex-col justify-between"
        self.plugin_dialog = PluginDialog(plugin)
        self.plugin = plugin
        self.install_toggle = None

    @ui.refreshable
    def render(self):
        browser_card = ui.card().classes(
            f"transition transform hover:scale-105 hover:border-blue-500 {self.base_card_classes}"
        )
        if DARK_MODE:
            browser_card.classes("dark-card")

        with browser_card:
            if self.plugin.logo:
                card_image = ui.image(self.plugin.logo).classes(
                    "w-full h-48 object-cover cursor-pointer"
                )
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(self.plugin.name.upper()).classes("text-lg font-bold")
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
        self.cpu_prog = 0.0
        self.mem_prog = 0.0
        self.disk_prog = 0.0
        self.chips = {}
        self.polling_task = None

    async def start_stats_polling(self, interval=2):
        try:
            while self.plugin.is_running:
                print("Polling")
                self.plugin.get_current_stats()
                self.update_stats_ui(self.plugin.current_stats)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print("Polling dead.")
        finally:
            self.polling_task = None

    @ui.refreshable
    async def render(self):
        self.plugin.get_current_stats()    
        if self.polling_task and not self.polling_task.done():
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                print("Polling task cancelled.")
        if self.plugin.is_running:
            self.polling_task = asyncio.create_task(self.start_stats_polling())
        installed_card = ui.card().classes(f"{self.base_card_classes}")
        if DARK_MODE:
            installed_card.classes(f"dark-card")
        with installed_card:
            with ui.row().classes("justify-between w-full"):
                ui.image(self.plugin.logo).classes("w-24 h-24")
                self.enable_toggle = ToggleButton(
                    on_label="Enable and Start",
                    off_label="Disable",
                    on_switch=self.plugin.run,
                    off_switch=self.plugin.stop,
                    state=not self.plugin.is_running,
                    on_color="secondary",
                    off_color="warning",
                ).classes("w-28 h-24")
            ui.label(self.plugin.name.upper()).classes("text-lg font-bold")
            ui.label(self.plugin.repo)
            ui.separator()
            if self.plugin.is_running:
                with ui.grid(columns=2).classes("text-xl"):
                    ui.markdown("**Status:**")
                    self.label_status = ui.label('Status Loading...').classes('text-lg font-semibold')
                    self.chips = {}
                    self.chips["Running"] = ui.chip("", color='running', text_color='white')
                    self.chips["Restarting"] = ui.chip("", color='restarting', text_color='white')
                    self.chips["Exited"] = ui.chip("", color='exited', text_color='white')
                    self.chips["Created"] = ui.chip("", color='created', text_color='white')
                    self.chips["Paused"] = ui.chip("", color='paused', text_color='white')
                    self.chips["Dead"] = ui.chip("", color='dead', text_color='white')
                self.update_status()
                ui.separator()
                await self.render_stats()
                ui.separator()
                with ui.row():
                    ui.button(
                        "UNINSTALL",
                        color="secondary",
                        on_click=lambda: self.uninstall_plugin(),
                    )
                    ui.button(
                        "VIEW LOGS", color="secondary", on_click=lambda: self.get_logs()
                    )
                    ui.button(
                        "EDIT", color="secondary", on_click=lambda: self.edit_env()
                    )
                    ui.button(
                        "RESTART",
                        color="secondary",
                        on_click=lambda: self.restart_plugin(),
                    )
                    ui.button(
                        "UPDATE",
                        color="secondary",
                        on_click=lambda: self.plugin.update(),
                    )

    @ui.refreshable
    async def render_stats(self):
        with ui.grid(columns=2).classes("w-full text-xl"):
            ui.markdown("CPU usage:")
            ui.linear_progress().bind_value(self, 'cpu_prog')
            ui.markdown("Memory usage:")
            ui.linear_progress().bind_value(self, 'mem_prog')
            ui.markdown("Disk usage:")
            ui.linear_progress().bind_value(self, 'disk_prog')

    def update_status(self):
        status = self.plugin.get_status()
        if isinstance(status, dict):
            for state in status.keys():
                if status[state] > 0:
                    self.chips[state].visible = True
                    self.chips[state].text = f'{state}: {status.get(state, 0)}'
                else:
                    self.chips[state].visible = False
            self.label_status.visible = False
        else:
            for state in self.chips.keys():
                self.chips[state].visible = False
            self.label_status.visible = True
            self.label_status.text = f'{status.title()}'
        if status == 'stopped':
            self.on = False
            self.label_status.classes('text-[#BF5234]')

    def uninstall_plugin(self):
        self.plugin.uninstall()

    def get_logs(self):
        logs_list = self.plugin.get_logs()
        if len(logs_list) == 0:
            ui.notify("No logs available for this plugin.")
            return
        with ui.dialog() as dialog:
            with ui.card():
                tab_names = list(logs_list.keys())
                with ui.tabs() as tabs:
                    for name in tab_names:
                        ui.tab(name)
                with ui.tab_panels(tabs, value=tab_names[0]) as panels:
                    for name in tab_names:
                        with ui.tab_panel(name):
                            ui.textarea(logs_list[name]).classes("w-full h-64").props("readonly")
                            ui.button(
                                "Download",
                                icon="download",
                                color="secondary",
                                on_click=lambda n=name: ui.download.text(logs_list[n], filename=f"{n}.txt"),
                            )
                with ui.row().classes("justify-end"):
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

    def update_stats_ui(self, stats):
        self.cpu_prog = stats['cpu'] / 100
        self.mem_prog = stats['memory'] / stats['memory_limit']
        self.disk_prog = stats['disk'] / 100
        self.render_stats.refresh()
    
    async def restart_plugin(self):
        await self.plugin.stop()
        print(self.plugin.is_running)
        await self.plugin.run()
