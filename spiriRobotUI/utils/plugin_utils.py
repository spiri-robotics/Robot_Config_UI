from nicegui import ui
from pathlib import Path
import os, yaml
from spiriRobotUI.utils.Plugin import Plugin, InstalledPlugin

plugins = {}
installed_plugins = {}

def load_plugins():
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    LIB_DIR = os.path.join(ROOT_DIR, 'spiriRobotUI', 'libs')
    plugin_list = os.path.join(LIB_DIR, 'plugins.yaml')

    with open(plugin_list, 'r') as f:
        file = yaml.safe_load(f)

    plugins.clear()

    for name, details in file.get('spiri-plugins').items():
        logo = details.get('logo')
        url = details.get('url')
        folder_name = details.get('folder_name')

        plug = Plugin(name, logo, url, folder_name)
        plugins[name] = plug

