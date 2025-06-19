from nicegui import ui

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer().classes('bg-white text-black'):
        with ui.column().classes('p-4'):
            ui.label('Spiri Robot UI').classes('text-2xl font-bold')
            ui.icon('diamond')
            ui.space
            ui.button('', icon='account_circle').classes('text-sm text-gray-600')
            ui.space
            ui.button('Home', icon='home').classes('w-full text-left')
            ui.button('Settings', icon='settings').classes('w-full text-left')
            ui.button('Help', icon='help').classes('w-full text-left')
        