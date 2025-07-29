from loguru import logger
from nicegui import ui

from SpiriRobotUI import layout
from SpiriRobotUI.components.page import Page

class SystemsMonitorPage(Page):
    """Page for managing systems monitoring."""

    priority = 1
    
    def __init__(self) -> None:
        """Initialize the systems monitoring page."""
        @ui.page("/system")
        def page_systems_monitor():
            with layout.frame("Systems Monitor"):
                ui.label("Systems Monitor Page").classes("text-h4 text-info")
        
    def draw_sidebar_item(self):
        """Draw the sidebar item for the systems monitor page."""
        ui.button("Systems Monitor", icon="monitor", color="primary", on_click=lambda: ui.navigate.to("/system")).classes("w-full")

extension = SystemsMonitorPage()