import os
import sys
import importlib
from loguru import logger

from SpiriRobotUI.components.singleton import SingletonMeta

class ExtensionLoader(metaclass=SingletonMeta):
    """Class to load and manage extensions for the SpiriRobotUI."""

    extension_registry = {}
    
    def __init__(self):
        """Initialize the extension loader."""
        self.extension_registry = {}
        logger.debug("Extension loader initialized.")

    async def load_extensions(self):
        """Load all extensions from the pages directory."""
        pages_dir = os.path.join(os.path.dirname(__file__), "pages")
        logger.debug(f"Looking for extensions in: {pages_dir}")
        
        for filename in os.listdir(pages_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                extension_name = f"SpiriRobotUI.pages.{filename[:-3]}"  # Remove the .py extension
                self.extension_registry[extension_name] = importlib.import_module(extension_name)
                # Debugging output to check which files are being processed
                if hasattr(self.extension_registry[extension_name], "extension"):
                    logger.debug(f"Loaded extension: {extension_name}")

        self.extension_registry = dict(sorted(self.extension_registry.items(), key=lambda item: getattr(item[1].extension, "priority", 0)))
