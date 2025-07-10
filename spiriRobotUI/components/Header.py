from nicegui import ui

def header() -> None:
    """Render the header."""
    with ui.button('').props('flat fab').classes('absolute top-4 right-4 z-50'):
        ui.icon('account_circle').classes('text-[#000000] dark:text-white')
    with ui.button('').props('flat fab').classes('absolute top-4 right-16 z-50'):
        ui.icon('more_vert').classes('text-[#000000] dark:text-white')
        