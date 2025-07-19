from nicegui import ui
from pathlib import Path
import os
from dotenv import dotenv_values

dotenv_path = Path(".env")
dotenv = dotenv_values(dotenv_path)

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer(value=True, top_corner=True, bottom_corner=True).props('width=297 breakpoint=200 bordered'):
        with ui.column().classes('w-full p-2'):
            with ui.row(align_items='center').classes('w-full justify-between pb-2'):
                ui.image("spiriRobotUI/icons/Spiri_logo_Mixed_dual_background.svg").classes('h-16 w-16')
                ui.label('Spiri Robot UI').classes('text-2xl font-semibold')
            
            ui.button('Plug-ins', color='secondary', on_click=lambda: ui.navigate.to("/")).classes('w-full')
            for variable in dotenv:
                if variable and variable.split('_')[0] == 'FEATURE':
                    feature_name = variable.split('_')[1]
                    feature_page = f"/{feature_name.lower()}"
                    ui.button(feature_name, color='secondary', on_click=lambda feature_page=feature_page: ui.navigate.to(feature_page)).classes('w-full')