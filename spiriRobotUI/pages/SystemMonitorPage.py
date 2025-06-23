from nicegui import ui
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header

@ui.page("/system")
async def system_ui():
    styles()
    sidebar()
    header()
    ui.markdown("## System Monitor")
    ui.label("Monitor your system performance and resource usage.")

    ui.separator()

    cpu_usage = 20

    ui.circular_progress(cpu_usage).classes('w-16 h-16')