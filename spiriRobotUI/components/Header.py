from nicegui import ui

def header() -> None:
    """Render the header."""
    with ui.header().classes('bg-white text-black flex justify-between items-center px-4'):
        ui.space()
        ui.button('', icon='more_vert').classes('text-sm text-gray-600')
        ui.button('', icon='account_circle').classes('text-sm text-black ml-auto')
        