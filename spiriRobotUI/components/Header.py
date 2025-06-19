from nicegui import ui

def header() -> None:
    """Render the header."""
    with ui.header().classes('bg-white text-black'):
        ui.label('Spiri Robot UI').classes('text-2xl font-bold')
        ui.icon('diamond')
        ui.space
        ui.button('', icon='account_circle').classes('text-sm text-gray-600')
        