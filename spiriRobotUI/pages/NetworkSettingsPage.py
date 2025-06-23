from nicegui import ui
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header

@ui.page("/network")
async def network_ui():
    styles()
    sidebar()
    header()
    ui.markdown("## Network Settings")
    ui.label("View and update your network settings with a few clicks.")

    ui.separator()

    cpu_usage = 20

    ui.circular_progress(cpu_usage).classes('w-16 h-16')