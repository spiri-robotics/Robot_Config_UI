from nicegui import ui

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer(top_corner=True, bottom_corner=True).classes('bg-white text-black'):
        with ui.column().classes('p-4'):
            with ui.row().classes('items-center justify-between'):
                ui.image("spiriRobotUI/icons/spiri_drone_ui_logo.svg").classes('h-12 w-12')
                ui.label('Spiri Robot UI').classes('text-2xl font-bold')
            ui.button('Plug-ins').classes('w-full text-left justify-start rounded-none')
            ui.button('Network Settings').classes('w-full text-left justify-start rounded-none')
            ui.button('System Monitor').classes('w-full text-left justify-start rounded-none')
        