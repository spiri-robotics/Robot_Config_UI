from nicegui import ui

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer(value=True, top_corner=True, bottom_corner=True).props('width=297 breakpoint=200 bordered'):
        with ui.column().classes('w-full p-2'):
            with ui.row(align_items='center').classes('w-full justify-between pb-2'):
                ui.image("spiriRobotUI/icons/Spiri_logo_Mixed_dual_background.svg").classes('h-16 w-16')
                ui.label('Spiri Robot UI').classes('text-2xl font-semibold')
            ui.button('Plug-ins', color='secondary', on_click=lambda: ui.navigate.to("/")).classes('w-full')
            ui.button('Network Settings', color='secondary', on_click=lambda: ui.navigate.to("/network")).classes('w-full')
            ui.button('System Monitor', color='secondary', on_click=lambda: ui.navigate.to("/system")).classes('w-full')
        