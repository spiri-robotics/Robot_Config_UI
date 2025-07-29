
from SpiriRobotUI.components.singleton import SingletonMeta

class Page(metaclass=SingletonMeta):
    """Base class for pages in the application."""

    priority = 1  # Default priority for page ordering

    def __init__(self) -> None:
        """Initialize the page."""
        pass

    def draw_sidebar_item(self):
        """Draw the sidebar item for the page."""
        raise NotImplementedError("draw_sidebar_item must be implemented in subclasses.")