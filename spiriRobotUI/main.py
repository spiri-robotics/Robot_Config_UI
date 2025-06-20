from nicegui import ui
from pathlib import Path
from spiriRobotUI.pages.PluginsPage import main_ui as plugins_page

favicon = "spiriRobotUI/icons/spiri_drone_ui_logo.svg"

ui.run(title='Robot Config UI',
        favicon=favicon,
        port=8080,
        show=True,
        uvicorn_reload_dirs=str(Path(__file__).parent.resolve()),
        reload=True,
       )