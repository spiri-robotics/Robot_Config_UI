import os

from pathlib import Path

INSTALLED_PLUGIN_DIR = Path(os.getenv('INSTALLED_PLUGIN_DIR', 'services'))
INSTALLED_PLUGIN_DIR.mkdir(exist_ok=True, parents=True)

PROJECT_ROOT = Path("~/robot-config-ui").resolve()