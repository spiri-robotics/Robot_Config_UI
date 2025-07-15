import cpuinfo, datetime, psutil, asyncio

from nicegui import ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.BindableObject import BindableObject
from spiriRobotUI.utils.styles import styles, style_vars

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

    with ui.tab_panels(tabs, value=system_tab).classes('w-full bg-transparent').props('animated=false'):
        with ui.tab_panel(system_tab):
            ui.markdown("## 🖥️ System Monitor")
                
            with ui.grid(columns=3, rows=2).classes('w-full'):

                # CPU Card
                with ui.card().classes('row-span-2'):
                    cpu_percent = psutil.cpu_percent(percpu=True)
                    avg = 0
                    for core in cpu_percent:
                        avg += core
                    avg /= len(cpu_percent)
                    
                    ui.label(f"🧠 CPU: {avg:.1f}%").classes('text-3xl font-bold text-[#274c77] dark:text-[#9EDFEC]')
                    info = cpuinfo.get_cpu_info()
                    ui.label(f"{info['brand_raw']}").classes('text-base')
                    freqs = psutil.cpu_freq(percpu=True)
                    with ui.grid(columns=2):
                        for i, freq in enumerate(freqs):
                            ui.label(f'Core {i+1}: ').classes('text-base')
                            ui.label(f'{cpu_percent[i]}% ({freq.current:.0f}MHz)').classes('text-base')
                    ui.label(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}")

                # Memory Card
                with ui.card():
                    mem = psutil.virtual_memory()
                    ui.label(f"💾 Memory: {mem.percent:.1f}%").classes('text-3xl font-bold text-[#274c77] dark:text-[#9EDFEC]')
                    ui.label(f"RAM: {format_bytes(mem.used)} / {format_bytes(mem.total)}").classes('text-base')
                    swap = psutil.swap_memory()
                    ui.label(f"SWAP: {format_bytes(swap.used)} / {format_bytes(swap.total)}").classes('text-base')
                    ui.label(f"🕒 {datetime.datetime.now().strftime('%H:%M:%S')}")

                # Temperature Card (with fallback)
                with ui.card().classes('row-span-2'):
                    ui.label("🌡️ Core Temperature").classes('text-3xl font-bold text-[#274c77] dark:text-[#9EDFEC]')
                    try:
                        temps = psutil.sensors_temperatures()
                        if "coretemp" in temps:
                            core_temps = temps["coretemp"]
                            for t in core_temps:
                                ui.label(f"{t.label}: {t.current:.1f}°C").classes('text-base')
                        elif temps:
                            for label, sensors in temps.items():
                                for t in sensors:
                                    ui.label(f"{label} {t.label}: {t.current:.1f}°C").classes('text-base')
                        else:
                            ui.label("Temperature data not available").classes('text-base')
                    except Exception as e:
                        ui.label("Temperature sensors unavailable").classes('text-base')
                        
                # Disk Card
                with ui.card():
                    disk = psutil.disk_usage('/')
                    ui.label(f"🗄️ Disk Usage: {disk.percent:.1f}%").classes('text-3xl font-bold text-[#274c77] dark:text-[#9EDFEC]')
                    ui.label(f"{format_bytes(disk.used)} / {format_bytes(disk.total)} used").classes('text-base')

        with ui.tab_panel(processes_tab):
            ui.markdown("## 🖥️ Processes")

        with ui.tab_panel(network_tab):
            ui.markdown("## 🖥️ Network")

        with ui.tab_panel(about_tab):
            ui.markdown("## 🖥️ About")