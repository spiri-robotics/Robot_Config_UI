from nicegui import ui
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header

@ui.page("/network")
async def network_ui():
    styles()
    sidebar()
    header()

    with ui.tabs().classes('w-full') as tabs:
        local_tab = ui.tab('LOCAL NETWORK TEST')
        internet_tab = ui.tab('INTERNET SPEED TEST')

    with ui.tab_panels(tabs, value=local_tab).classes('w-full'):

        with ui.tab_panel(local_tab):
            ui.markdown("## Local Network Speed and Latency Test")

            with ui.row().classes('items-center justify-between'):
                circular = ui.circular_progress(0.0).classes('w-40 h-40')
                with ui.column():
                    ui.icon('cloud_download').classes('text-white')
                    download_label = ui.label('... Mbps')
                    ui.icon('cloud_upload').classes('text-white')
                    upload_label = ui.label('... Mbps')
                    ui.icon('timer').classes('text-white')
                    latency_label = ui.label('... ms')

            # Graph area
            with ui.card().classes('bg-gray-800 w-full'):
                ui.label('Speed (Mbps)').classes('text-white')
                chart = ui.line_chart({'x': [], 'y': []}).classes('h-48 w-full')

            # Start Button
            async def start_test():
                # Replace this logic with real test integration
                circular.set_value(42)
                download_label.text = "95.4 Mbps"
                upload_label.text = "35.2 Mbps"
                latency_label.text = "12 ms"
                chart.update({'x': list(range(10)), 'y': [i * 10 for i in range(10)]})

            ui.button(icon='play_arrow', on_click=start_test).classes('mt-4')

        with ui.tab_panel(internet_tab):
            ui.label("Internet speed test coming soon...")