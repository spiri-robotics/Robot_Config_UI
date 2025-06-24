from pathlib import Path

from nicegui import ui

from spiriRobotUI.pages.NetworkSettingsPage import network_ui as network_settings_page
from spiriRobotUI.pages.PluginsPage import main_ui as plugins_page
from spiriRobotUI.pages.SystemMonitorPage import system_ui as system_monitor_page
from spiriRobotUI.utils.styles import DARK_MODE

favicon = "spiriRobotUI/icons/spiri_drone_ui_logo.svg"
ui.run(title='Robot Config UI',
    favicon=favicon,
    port=8089,
    show=True,
    dark=DARK_MODE,
    uvicorn_reload_dirs=str(Path(__file__).parent.resolve()),
    reload=True,
)