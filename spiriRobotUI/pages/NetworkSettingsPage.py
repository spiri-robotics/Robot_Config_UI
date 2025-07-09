from nicegui import ui
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header
import speedtest
import asyncio

@ui.page("/network")
async def network_ui():
    await styles()
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

            chart = ui.echart({
                'xAxis': {'type': 'category', 'data': []},
                'yAxis': {'type': 'value'},
                'series': [{
                    'data': [],
                    'type': 'line'
                }]
            }).classes('h-64 w-full')

            
            def run_speedtest():
                st = speedtest.Speedtest()
                st.get_servers([])
                best = st.get_best_server()
                st.download()
                st.upload()
                return {
                    'latency': best['latency'],
                    'download': st.results.download / 1_000_000,
                    'upload': st.results.upload / 1_000_000,
                }

            async def start_test():
                circular.set_value(0)
                download_label.text = "... Mbps"
                upload_label.text = "... Mbps"
                latency_label.text = "... ms"
                chart.options['xAxis']['data'] = []
                chart.options['series'][0]['data'] = []
                chart.update()

                latency_label.text = "Finding server..."
                await asyncio.sleep(0.5)

                results = await asyncio.to_thread(run_speedtest)

                latency_label.text = f"{results['latency']:.0f} ms"
                download_label.text = "Testing download..."
                upload_label.text = "Testing upload..."

                speeds = []
                x_data = []
                for i in range(1, 11):
                    partial_speed = min(results['download'], i * (results['download'] / 10))
                    speeds.append(round(partial_speed, 1))
                    x_data.append(f"{i * 0.5:.1f}s")
                    circular.set_value(partial_speed / 100)
                    chart.options['xAxis']['data'] = x_data
                    chart.options['series'][0]['data'] = speeds
                    chart.update()
                    await asyncio.sleep(0.3)

                download_label.text = f"{results['download']:.1f} Mbps"
                upload_label.text = f"{results['upload']:.1f} Mbps"

            ui.button(icon='play_arrow', on_click=start_test).classes('mt-4')

        with ui.tab_panel(internet_tab):
            ui.label("Internet speed test coming soon...")