from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.PluginCard import PluginBrowserCard, PluginInstalledCard
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.Plugin import InstalledPlugin, Plugin, plugins, installed_plugins
from spiriRobotUI.utils.plugin_utils import load_plugins, load_installed, save_new_plugin
from spiriRobotUI.utils.styles import styles

installed_cards = []
browser_cards = []
def add_new_plugin_card(plugin: Plugin):
    new_card = PluginBrowserCard(plugin)
    new_card.render()

def add_installed_card(plugin: InstalledPlugin):
    new_card = PluginInstalledCard(plugin)
    new_card.render()

@ui.page("/")
async def main_ui():

    await styles()
    sidebar()
    header()

    with ui.dialog() as d, ui.card().classes('p-5 justify-center w-full'):
        ui.label('Link A Plugin').classes('text-h5')
        link = ui.input('Repository link', placeholder='www.git.spirirobotics.com/your-repo').classes('w-full')
        check = ui.checkbox('Install all plugins in repository', value=False)
        with ui.row().classes('justify-center w-full'):
            ui.button('go away', color='secondary', on_click=lambda: d.submit(None))
            ui.button('submit', color='secondary', on_click=lambda l=link, c=check: submit(l, c))

    def submit(link: ui.input, check: ui.checkbox):
        d.submit([link.value, check.value])
        check.clear()

    async def new_plugin():
        form = await d
        if form is None:
            pass
        else:
            link = form[0]
            check = form[1]

            if link is not None:
                print(check)
                save_new_plugin(link, check)

    ui.markdown("## Plug-in Coordinator")
    with ui.row(align_items='end').classes('w-full justify-between'):
        ui.label("Your favourite plugins, now all in one place.")
        ui.button('Link plugin', color='secondary', on_click=new_plugin)

    ui.separator()

    load_plugins()
    load_installed()

    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Available')
        two = ui.tab('Installed')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                for plug in plugins.values():
                    p = PluginBrowserCard(plug)
                    p.render()
        with ui.tab_panel(two):
            if len(installed_plugins) == 0:
                ui.label("No plugins installed yet. Please visit the 'Available' tab to install plugins.")
            else:
                with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                    for plug in installed_plugins.values():
                        p = PluginInstalledCard(plug)
                        p.render()
@ui.refreshable
def browser_grid_ui():
    with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
        for plug in plugins.values():
            p = PluginBrowserCard(plug)
            p.render()