from nicegui import ui
from pathlib import Path
import yaml, os
from spiriRobotUI.utils.Plugin import Plugin, InstalledPlugin
from spiriRobotUI.settings import INSTALLED_PLUGIN_DIR

plugins = {}
installed_plugins = {}

ROOT_DIR = Path(__file__).parents[2].absolute()
LIB_DIR = ROOT_DIR / 'spiriRobotUI' / 'libs'
ICON_DIR = ROOT_DIR / 'spiriRobotUI' / 'icons'
REPO_DIR = ROOT_DIR / 'repos'

def load_plugins():
    plugin_list = LIB_DIR / 'plugins.yaml'

    if not plugin_list.exists():
        print('No plugins.yaml file found')
        return
    
    with open(plugin_list, 'r') as f:
        file = yaml.safe_load(f)

    plugins.clear()

    print(file)

    for name, details in file.get('spiri-plugins').items():
        logo = details.get('logo')
        url = details.get('url')
        repo = details.get('repo')
        versions = details.get('versions')

        plug = Plugin(name, logo, url, repo, versions)
        plugins[name] = plug

# def get_details(service: Path) -> dict:
#     details = {}
#     details['name'] = service.name

#     logo = service / 'logo.jpg'
#     if not logo.exists():
#         logo = ICON_DIR / 'ConfigUILogo.png'
#     details['logo'] = str(logo)

#     url = 
#     return details

def load_installed():
    for folder in INSTALLED_PLUGIN_DIR.iterdir():
        if not folder.is_dir:
            print('not a folder')
            continue