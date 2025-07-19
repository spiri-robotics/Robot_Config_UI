from nicegui import app, ui, Client
import asyncio
from spiriRobotUI.components.PluginDialog import PluginDialog
from spiriRobotUI.components.ToggleButton import ToggleButton
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin
from spiriRobotUI.utils.EventBus import event_bus
from spiriRobotUI.utils.styles import style_vars
from spiriRobotUI.utils.system_utils import disk

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
                ui.label(self.plugin.name.replace('_', ' ').replace('-', ' ').title()).classes("text-lg font-medium pb-4")
                self.install_toggle = ToggleButton(
                    on_label="Uninstall",
                    off_label="Install",
                    on_switch=lambda: self.plugin.uninstall(),
                    off_switch=lambda: self.plugin.install(),
                    state=self.plugin.is_installed,
                    on_color="negative",
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
        plugin.get_current_stats()
        self.stats = plugin.current_stats
        self.chips = {}
        self.polling_task = None

    async def start_stats_polling(self, interval=2):
        while self.plugin.is_running:
            self.plugin.get_current_stats()
            self.update_stats()
            await asyncio.sleep(interval)

    @ui.refreshable
    async def render(self):
        if self.plugin.is_running:
            self.polling_task = asyncio.create_task(self.start_stats_polling())
        elif self.polling_task != None:
            self.polling_task.cancel()
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
                        on_color="negative",
                        off_color="positive",
                    ).classes("w-32 h-24")
            
            with ui.card_section().classes('w-full'):
                ui.label(self.plugin.name.replace('_', ' ').replace('-', ' ').title()).classes("text-xl font-medium")
                ui.label(self.plugin.repo).classes('text-base font-light')
            
            if self.plugin.is_running:
                ui.separator()
                
                with ui.card_section().classes('w-full'):
                    with ui.row().classes('justify-between items-center'):
                        ui.label("Status:").classes('font-medium')
                        self.label_status = ui.label('Status Loading...').classes('font-medium')
                        self.chips = {}
                        self.chips["Running"] = ui.chip("", color='running', text_color='white').classes('text-center')
                        self.chips["Restarting"] = ui.chip("", color='restarting', text_color='white')
                        self.chips["Exited"] = ui.chip("", color='exited', text_color='white')
                        self.chips["Created"] = ui.chip("", color='created', text_color='white')
                        self.chips["Paused"] = ui.chip("", color='paused', text_color='white')
                        self.chips["Dead"] = ui.chip("", color='dead', text_color='white')
                self.update_status()
                
                ui.separator()
                with ui.card_section().classes('w-full'):
                    await self.render_stats()
                ui.separator()
                
                with ui.card_section().classes('w-full'):
                    with ui.grid(rows=2, columns=2):
                        if self.plugin.repo:
                            ui.button("EDIT", color='secondary', on_click=lambda: self.edit_env())
                            ui.button("UPDATE", color='secondary', on_click=lambda: self.plugin.update())
                            ui.button("VIEW LOGS", color='secondary', on_click=lambda: self.get_logs())
                            ui.button("RESTART", color='secondary', on_click=lambda: self.restart_plugin())
                        else:
                            ui.button("EDIT", color='secondary', on_click=lambda: self.edit_env())
                            ui.button("VIEW LOGS", color='secondary', on_click=lambda: self.get_logs())
                            ui.button("RESTART", color='secondary', on_click=lambda: self.restart_plugin()).classes('col-span-2')
                        
            else:
                ui.space()
                with ui.card_section().classes('w-full'):
                    if self.plugin.repo:
                        with ui.grid(rows=2, columns=2):
                            ui.button("EDIT", color='secondary', on_click=lambda: self.edit_env())
                            ui.button("UPDATE", color='secondary', on_click=lambda: self.plugin.update())
                            ui.button("UNINSTALL", color='negative', on_click=lambda: self.uninstall_plugin()).classes('col-end-[span_2]')
                    else:
                        with ui.grid(columns=2):
                            ui.button("EDIT", color='secondary', on_click=lambda: self.edit_env())
                            ui.button("UNINSTALL", color='negative', on_click=lambda: self.uninstall_plugin()).classes('col-end-[span_2]')
                    
    @ui.refreshable
    async def render_stats(self):
        with ui.grid(columns=2).classes("w-full font-medium items-center"):
            ui.markdown("CPU usage:")
            ui.label().bind_text_from(self.stats, 'cpu', backward=lambda stats: f"{str(stats)[0:4]}%")
            ui.markdown("Memory usage:")
            ui.label().bind_text_from(self.stats, 'memory', backward=lambda stats: f"{str(stats)[0:4]} GB / {str(self.stats['memory_limit'])[0:4]} GB")

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
        else:
            self.label_status.classes(remove='text-[#BF5234]')

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
                            ui.code(logs_list[name], language='text').classes("w-full h-64 overflow-auto")
                            ui.button(
                                "Download",
                                icon="download",
                                color="secondary",
                                on_click=lambda n=name: ui.download.content(logs_list[n], f"{n}.txt"),
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

    def update_stats(self):
        new_stats = self.plugin.current_stats
        for k, v in new_stats.items():
            self.stats[k] = v
    
    async def restart_plugin(self):
        await self.plugin.stop()
        print(self.plugin.is_running)
        await self.plugin.run()
