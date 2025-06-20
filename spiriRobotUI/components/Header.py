from nicegui import ui

def header() -> None:
    """Render the header."""
    ui.button('', icon='account_circle').props('flat fab color=black').classes('absolute top-4 right-4 z-50')
    ui.button('', icon='more_vert').props('flat fab color=black').classes('absolute top-4 right-16 z-50')
        