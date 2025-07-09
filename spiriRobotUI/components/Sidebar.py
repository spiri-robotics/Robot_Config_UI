from nicegui import ui

def test() -> None:
    """Test function to ensure the module is loaded correctly."""
    print("Sidebar module loaded successfully.")

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer(value=True, top_corner=True, bottom_corner=True).classes('bg-white text-black').props('behavior=desktop'):
        with ui.column().classes('p-4'):
            with ui.row().classes('items-center justify-between pb-[--nicegui-default-padding]'):
                ui.image("spiriRobotUI/icons/spiri_drone_ui_logo.svg").classes('h-12 w-12')
                ui.label('Spiri Robot UI').classes('text-2xl font-bold')
            ui.button('Plug-ins', color='secondary', on_click=lambda: ui.navigate.to("/")).classes('w-full text-left justify-start rounded-none')
            ui.button('Network Settings', color='secondary', on_click=lambda: ui.navigate.to("/network")).classes('w-full text-left justify-start rounded-none')
            ui.button('System Monitor', color='secondary', on_click=lambda: ui.navigate.to("/system")).classes('w-full text-left justify-start rounded-none')
        