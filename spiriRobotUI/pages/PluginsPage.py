from nicegui import ui
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header

plugins = {
    "plugin1": {
        "name": "Plugin 1",
        "description": "This is the first plugin.",
        "url": "https://example.com/plugin1"
    } }      

def add_new_plugin_card(plugin):
    """Add a new plugin card to the UI."""
    with ui.card().classes("p-4 bg-white shadow-md rounded-lg"):
            ui.label(plugin["name"]).classes("text-lg font-bold")
            ui.markdown(plugin["description"]).classes("text-sm text-gray-600")
                
@ui.page("/")
async def main_ui():
    sidebar()
    header()
    ui.markdown("## Plug-in Coordinator")
    ui.label("Your favourite plugins, now all in one place.")

    ui.separator()

    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Available')
        two = ui.tab('Installed')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                for plugin_name in plugins:
                        add_new_plugin_card(plugins[plugin_name])
        with ui.tab_panel(two):
            ui.label("No plugins installed yet. Please visit the 'Available' tab to install plugins.")
            with ui.grid().classes("grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"):
                for plugin_name in plugins:
                        add_new_plugin_card(plugins[plugin_name])