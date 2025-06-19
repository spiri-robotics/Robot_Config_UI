from nicegui import ui

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer(top_corner=True, bottom_corner=True).classes('bg-white text-black'):
        with ui.column().classes('p-4'):
            with ui.row().classes('items-center justify-between'):
                ui.icon('diamond')
                ui.label('Spiri Robot UI').classes('text-2xl font-bold')
            ui.button('Plugins', icon='home').classes('w-full text-left justify-start rounded-none')
            ui.button('Netowork Settings', icon='settings').classes('w-full text-left justify-start rounded-none')
        