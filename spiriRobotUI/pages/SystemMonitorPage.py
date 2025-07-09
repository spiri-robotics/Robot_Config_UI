from nicegui import ui
from spiriRobotUI.utils.styles import styles
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.components.Header import header
from nicegui import ui
import psutil
import cpuinfo
import datetime

def format_bytes(bytes_val):
    return f"{bytes_val / (1024 ** 3):.1f} GB"

@ui.page("/system")
async def system_ui():
    await styles()
    sidebar()
    header()
    
    with ui.tabs().classes('w-full') as tabs:
        system_tab = ui.tab('SYSTEM MONITOR')
        processes_tab = ui.tab('PROCESSES')
        network_tab = ui.tab('NETWORK')
        about_tab = ui.tab('ABOUT')

    with ui.tab_panels(tabs, value=system_tab).classes('w-full'):
        with ui.tab_panel(system_tab):
            ui.markdown("## 🖥️ System Monitor")

            with ui.row().classes('w-full justify-around'):

                # CPU Card
                with ui.card().classes('w-1/2 bg-gray-900 text-white'):
                    cpu_percent = psutil.cpu_percent(percpu=False)
                    ui.label(f"🧠 {cpu_percent:.1f}%").classes('text-3xl font-bold text-center text-blue-400')
                    info = cpuinfo.get_cpu_info()
                    ui.label(f"{info['brand_raw']}").classes('text-sm')
                    freqs = psutil.cpu_freq(percpu=True)
                    for i, freq in enumerate(freqs):
                        ui.label(f"cpu{i}: {psutil.cpu_percent(percpu=True)[i]}% ({freq.current:.0f}MHz)")

                    ui.label(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}").classes('text-xs')

                # Memory Card
                with ui.card().classes('w-1/2 bg-gray-900 text-white'):
                    mem = psutil.virtual_memory()
                    ui.label(f"💾 {mem.percent:.1f}%").classes('text-3xl font-bold text-center text-blue-400')
                    ui.label("Memory").classes('text-sm')
                    ui.label(f"RAM: {format_bytes(mem.used)} / {format_bytes(mem.total)}")
                    swap = psutil.swap_memory()
                    ui.label(f"SWAP: {format_bytes(swap.used)} / {format_bytes(swap.total)}")
                    ui.label(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}").classes('text-xs')

            with ui.row().classes('w-full justify-around mt-4'):

                # Disk Card
                with ui.card().classes('w-1/2 bg-gray-900 text-white'):
                    disk = psutil.disk_usage('/')
                    ui.label(f"🗄️ {disk.percent:.1f}%").classes('text-3xl font-bold text-center text-blue-400')
                    ui.label("Disk").classes('text-sm')
                    ui.label(f"{format_bytes(disk.used)} / {format_bytes(disk.total)} used")

                # Temperature Card (with fallback)
                with ui.card().classes('w-1/2 bg-gray-900 text-white'):
                    ui.label("🌡️ Loading.. °C").classes('text-3xl font-bold text-center text-blue-400')
                    try:
                        temps = psutil.sensors_temperatures()
                        if "coretemp" in temps:
                            core_temps = temps["coretemp"]
                            for t in core_temps:
                                ui.label(f"{t.label}: {t.current:.1f}°C")
                        elif temps:
                            for label, sensors in temps.items():
                                for t in sensors:
                                    ui.label(f"{label} {t.label}: {t.current:.1f}°C")
                        else:
                            ui.label("Temperature data not available")
                    except Exception as e:
                        ui.label("Temperature sensors unavailable").classes('text-xs')

        with ui.tab_panel(processes_tab):
            ui.markdown("## 🖥️ Processes")

        with ui.tab_panel(network_tab):
            ui.markdown("## 🖥️ Network")

        with ui.tab_panel(about_tab):
            ui.markdown("## 🖥️ About")