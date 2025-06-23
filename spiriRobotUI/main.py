from pathlib import Path
from nicegui import ui
from spiriRobotUI.components.Header import header
from spiriRobotUI.components.store import home
from spiriRobotUI.ui.styles import styles
from spiriRobotUI.classes.PluginCard import PluginStoreCard, PluginInstalledCard
from spiriRobotUI.classes.Plugin import Plugin, InstalledPlugin

favicon = """
<svg viewBox="0 0 41.757 41.629" xmlns="http://www.w3.org/2000/svg"><g stroke-linecap="round"><path d="M13.069.128A12.813 12.813 0 0 0 .256 12.941 12.813 12.813 0 0 0 13.07 25.753a13 13 0 0 0 2.255-.224 7.3 7.3 0 0 1-1.776-4.772 7.303 7.303 0 0 1 7.303-7.304 7.3 7.3 0 0 1 4.795 1.797 13 13 0 0 0 .236-2.31A12.813 12.813 0 0 0 13.07.129" fill="#dd5935"/><path d="M28.415.128a12.813 12.813 0 0 0-12.813 12.813 13 13 0 0 0 .275 2.488 7.3 7.3 0 0 1 4.974-1.976 7.303 7.303 0 0 1 7.304 7.304 7.3 7.3 0 0 1-1.813 4.812 13 13 0 0 0 2.073.184 12.813 12.813 0 0 0 12.813-12.812A12.813 12.813 0 0 0 28.415.128" fill="#899ca3"/><path d="M28.944 16.003a13 13 0 0 0-2.35.245 7.3 7.3 0 0 1 1.56 4.509 7.303 7.303 0 0 1-7.303 7.303 7.3 7.3 0 0 1-4.482-1.56 13 13 0 0 0-.238 2.316 12.813 12.813 0 0 0 12.813 12.812 12.813 12.813 0 0 0 12.813-12.812 12.813 12.813 0 0 0-12.813-12.813" fill="#fac529"/><path d="M3.047 20.878a12.8 12.8 0 0 0-2.79 7.938 12.813 12.813 0 0 0 12.812 12.813 12.813 12.813 0 0 0 12.813-12.813 13 13 0 0 0-.277-2.518 7.3 7.3 0 0 1-4.754 1.762 7.3 7.3 0 0 1-5.528-2.532 13 13 0 0 1-2.254.226 12.81 12.81 0 0 1-10.022-4.876" fill="#9edfec"/><path d="M12.813 0A12.813 12.813 0 0 0 0 12.813a12.81 12.81 0 0 0 7.272 11.535 13.8 13.8 0 0 1-.553-3.858A13.77 13.77 0 0 1 20.49 6.72a13.8 13.8 0 0 1 3.877.56A12.81 12.81 0 0 0 12.813 0" fill="#fac529"/><path d="M28.688 0a12.81 12.81 0 0 0-11.466 7.143 13.8 13.8 0 0 1 3.268-.424A13.77 13.77 0 0 1 34.261 20.49a13.8 13.8 0 0 1-.65 4.127 12.81 12.81 0 0 0 7.89-11.804A12.813 12.813 0 0 0 28.688 0" fill="#9edfec"/><path d="M33.792 16.939a13.8 13.8 0 0 1 .47 3.551A13.77 13.77 0 0 1 20.49 34.261a13.8 13.8 0 0 1-3.544-.485A12.81 12.81 0 0 0 28.688 41.5 12.813 12.813 0 0 0 41.5 28.688a12.81 12.81 0 0 0-7.71-11.749" fill="#dd5935"/><path d="M2.79 20.75A12.8 12.8 0 0 0 0 28.688 12.813 12.813 0 0 0 12.813 41.5a12.81 12.81 0 0 0 11.83-7.9 13.8 13.8 0 0 1-4.153.66 13.77 13.77 0 0 1-13.225-9.946A12.8 12.8 0 0 1 2.79 20.75" fill="#899ca3"/></g></svg>"""

@ui.page("/")
async def main_ui():
    styles()
    header()

    with ui.splitter(value=8).props('disable').classes('w-full') as splitter:
        with splitter.before:
            with ui.tabs().props('vertical inline-label align="left" active-bg-color="primary"').classes('w-full ') as tabs:
                with ui.tab("hm", label='').classes('justify-start') as home_tab:
                    with ui.row(align_items='center'):
                        ui.icon('apps').classes('text-2xl')
                        ui.label('Store').classes('font-medium')
                with ui.tab("in", label='').classes('justify-start') as installed_tab:
                    with ui.row(align_items='center'):
                        ui.icon('folder').classes('text-2xl')
                        ui.label('Installed').classes('font-medium')
                with ui.tab("s", label='').classes('justify-start') as settings_tab:
                    with ui.row(align_items='center'):
                        ui.icon('settings').classes('text-2xl')
                        ui.label('Settings').classes('font-medium')
                with ui.tab("hp", label='').classes('justify-start') as help_tab:
                    with ui.row(align_items='center'):
                        ui.icon('help').classes('text-2xl')
                        ui.label('Help').classes('font-medium')

        with splitter.after:
            with ui.tab_panels(tabs, value=home_tab).props('vertical animated="false"').classes('w-full'):
                with ui.tab_panel(home_tab):
                    await home()
                with ui.tab_panel(installed_tab):
                    ui.label('installed tab')
                with ui.tab_panel(settings_tab):
                    ui.label('settings tab')
                with ui.tab_panel(help_tab):
                    ui.label('help tab')


ui.run(
    title="Robot Config UI",
    favicon=favicon,
    port=8089,
    show=True,
    uvicorn_reload_dirs=str(Path(__file__).parent.resolve()),
    reload=True,
)
