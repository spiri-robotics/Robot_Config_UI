from nicegui import ui

def header() -> None:
    """Render the header."""
    with ui.header().classes('bg-white text-black flex justify-between items-center px-4'):
        ui.space()
        ui.button('', icon='more_vert').classes('bg-transparent shawdow-none text-sm text-black')
        ui.button('', icon='account_circle').classes('bg-transparent shadow-none text-sm text-black ml-auto')
        