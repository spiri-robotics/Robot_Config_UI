from nicegui import ui, app

from SpiriRobotUI.extension_loader import ExtensionLoader

extension_loader = ExtensionLoader()
app.on_startup(extension_loader.load_extensions())

ui.run(
    port=8089,
    title="Robot Config UI",
    favicon="SpiriRobotUI/icons/spiri_drone_ui_logo.svg",
    dark=None,
    show=False,
    reload=True,
)