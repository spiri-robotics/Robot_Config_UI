from loguru import logger
from nicegui import ui

from SpiriRobotUI import layout
from SpiriRobotUI.components.page import Page

class PluginsPage(Page):
    """Page for managing plugins."""

    priority = 0

    def __init__(self) -> None:
        """Initialize the plugins page."""
        @ui.page("/")
        def page_plugins():
            with layout.frame("Plugins"):
                ui.label("Plugins Page").classes("text-h4 text-info")
        
    def draw_sidebar_item(self):
        """Draw the sidebar item for the plugins page."""
        ui.button("Plug-ins", icon="extension", color="primary", on_click=lambda: ui.navigate.to("/")).classes("w-full")

extension = PluginsPage()