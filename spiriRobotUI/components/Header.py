from nicegui import ui

def header() -> None:
    """Render the header."""
    with ui.header().classes('bg-white text-black items-center'):
        ui.label('Spiri Robot UI').classes('text-2xl font-bold')
        ui.icon('diamond').classes('text-xl')
        ui.space()
        ui.button(icon='account_circle', color='secondary').classes('text-sm text-gray-600')
        