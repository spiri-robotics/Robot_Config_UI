from nicegui import ui

logo = """<svg viewBox="0 0 41.5 41.5" xmlns="http://www.w3.org/2000/svg"><g stroke-width=".86" stroke-linecap="round"><path d="M27.22 2.86a11 11 0 0 0-9.7 6.3 12 12 0 0 1 2.79-.42 11.8 11.8 0 0 1 12 11.57 12 12 0 0 1-.49 3.55 11 11 0 0 0 6.57-10.23A10.97 10.97 0 0 0 27.22 2.86" fill="#9edfec"/><path d="M30.87 9.56a11 11 0 0 0-4.32.68 11.9 11.9 0 0 1 5.86 10.27 11.9 11.9 0 0 1-5.9 10.25 11 11 0 0 0 11.8-2.69 10.97 10.97 0 0 0-.4-15.5 11 11 0 0 0-7.04-3.01" fill="#fac529"/><path d="M31.85 17.28a12 12 0 0 1 .46 3.03 11.8 11.8 0 0 1-11.57 12 12 12 0 0 1-3.04-.35 11 11 0 0 0 10.17 6.43 10.97 10.97 0 0 0 10.77-11.17 11 11 0 0 0-6.79-9.94" fill="#dd5935"/><path d="M31.04 25.98a11.9 11.9 0 0 1-10.54 6.44 11.9 11.9 0 0 1-9.95-5.38 11 11 0 0 0 2.88 11.27 10.97 10.97 0 0 0 15.5-.4 11 11 0 0 0 2.11-11.93" fill="#9edfec"/><path d="M5.38 21.03a11 11 0 0 0-2.27 6.84 10.97 10.97 0 0 0 11.17 10.77 11 11 0 0 0 10-6.95 12 12 0 0 1-3.54.63 11.8 11.8 0 0 1-11.48-8.3 11 11 0 0 1-3.88-2.99" fill="#899ca3"/><path d="M11.65 10.04a11 11 0 0 0-8.46 3.39 10.97 10.97 0 0 0 .39 15.5 11 11 0 0 0 11.66 2.24A11.9 11.9 0 0 1 8.58 20.5a11.9 11.9 0 0 1 5.52-10.04 11 11 0 0 0-2.45-.42" fill="#dd5935"/><path d="M13.37 3.24A10.97 10.97 0 0 0 2.61 14.41 11 11 0 0 0 9 24.17a12 12 0 0 1-.53-3.3 11.8 11.8 0 0 1 11.57-12 12 12 0 0 1 3.33.42l-.13-.22a12 12 0 0 0-2.94-.33 12 12 0 0 0-2.8.42 11 11 0 0 1 2.75-3.62 11 11 0 0 0-6.89-2.3" fill="#fac529"/><path d="M21.02.19a11 11 0 0 0-8.46 3.4 11 11 0 0 0-2.41 11.07 12 12 0 0 1 7.48-5.7 11 11 0 0 1 9.59-6.1l.49.03A11 11 0 0 0 21 .19" fill="#899ca3"/></g></svg>"""

def sidebar() -> None:
    """Render the sidebar."""
    with ui.left_drawer(top_corner=True, bottom_corner=True).classes('bg-white text-black'):
        with ui.column().classes('p-4'):
            with ui.row().classes('items-center justify-between'):
                ui.image("spiriRobotUI/icons/ConfigUILogo.png").classes('h-12 w-12')
                ui.label('Spiri Robot UI').classes('text-2xl font-bold')
            ui.button('Plug-ins').classes('w-full text-left justify-start rounded-none')
            ui.button('Network Settings').classes('w-full text-left justify-start rounded-none')
            ui.button('System Monitor').classes('w-full text-left justify-start rounded-none')
        