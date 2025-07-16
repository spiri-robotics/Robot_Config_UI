import cpuinfo, datetime, psutil, asyncio

from nicegui import app, ui

from spiriRobotUI.components.Header import header
from spiriRobotUI.components.Sidebar import sidebar
from spiriRobotUI.utils.styles import styles

def format_bytes(bytes_val):
    return f"{bytes_val / (1024 ** 3):.1f} GB"

system_stats = {
    'cpu_percent': psutil.cpu_percent(percpu=False),
    'core_percents': psutil.cpu_percent(percpu=True),
    'cpu_freq': psutil.cpu_freq(percpu=True),
    'mem_percent': psutil.virtual_memory().percent,
    'mem_used': psutil.virtual_memory().used,
    'mem_total': psutil.virtual_memory().total,
    'swap_used': psutil.swap_memory().used,
    'swap_total': psutil.swap_memory().total,
    'disk': psutil.disk_usage('/'),
    'temps': psutil.sensors_temperatures(),
    'core_temps': None
}

@ui.page("/system")
async def system_ui():
    await styles()
    sidebar()
    header()
    asyncio.create_task(system_stats_polling())
    with ui.tabs().classes('w-full') as tabs:
        system_tab = ui.tab('SYSTEM MONITOR')
        processes_tab = ui.tab('PROCESSES')
        network_tab = ui.tab('NETWORK')
        about_tab = ui.tab('ABOUT')

    with ui.tab_panels(tabs, value=system_tab).classes('w-full'):
        with ui.tab_panel(system_tab):
            ui.markdown("## 🖥️ System Monitor")
            sys_monitor_ui()
            if 'coretemp' in system_stats['temps']:
                system_stats['core_temps'] = system_stats['temps']["coretemp"]

        with ui.tab_panel(processes_tab):
            ui.markdown("## 🖥️ Processes")

        with ui.tab_panel(network_tab):
            ui.markdown("## 🖥️ Network")

        with ui.tab_panel(about_tab):
            ui.markdown("## 🖥️ About")

@ui.refreshable
def sys_monitor_ui():
    with ui.row().classes('w-full justify-around'):

        # CPU Card
        with ui.card().classes('w-1/2 bg-gray-900 text-white'):
            ui.label().bind_text_from(system_stats, 'cpu_percent', backward=lambda stats: f"🧠 {stats:.1f}%").classes('text-3xl font-bold text-center text-blue-400')
            info = cpuinfo.get_cpu_info()
            ui.label(f"{info['brand_raw']}").classes('text-sm')
            with ui.grid(columns=2):
                for i, freq in enumerate(system_stats['cpu_freq']):
                    ui.label(f'Core {i+1}: ').classes('text-base')
                    ui.label().bind_text_from(
                        system_stats,
                        'core_percents',
                        backward=lambda stats, freq=freq, i=i: f'{stats[i]}% ({freq.current:.0f}MHz)'
                    ).classes('text-base')

        # Memory Card
        with ui.card().classes('w-1/2 bg-gray-900 text-white'):
            ui.label().bind_text_from(system_stats, 'mem_percent', backward=lambda stats: f"💾 {stats:.1f}%").classes('text-3xl font-bold text-center text-blue-400')
            ui.label("Memory").classes('text-sm')
            ui.label().bind_text_from(system_stats, 'mem_used', backward=lambda stats: f"RAM: {format_bytes(stats)} / {format_bytes(system_stats['mem_total'])}")
            ui.label().bind_text_from(system_stats, 'swap_used', backward=lambda stats: f"SWAP: {format_bytes(stats)} / {format_bytes(system_stats['swap_total'])}")

    with ui.row().classes('w-full justify-around mt-4'):

        # Disk Card
        with ui.card().classes('w-1/2 bg-gray-900 text-white'):
            disk = psutil.disk_usage('/')
            ui.label().bind_text_from(system_stats, 'disk', backward=lambda stats: f"🗄️ {stats.percent:.1f}%").classes('text-3xl font-bold text-center text-blue-400')
            ui.label("Disk").classes('text-sm')
            ui.label().bind_text_from(system_stats, 'disk', backward=lambda stats: f"{format_bytes(stats.used)} / {format_bytes(stats.total)} used")

        # Temperature Card (with fallback)
        with ui.card().classes('w-1/2 bg-gray-900 text-white'):
            ui.label("🌡️ Loading.. °C").classes('text-3xl font-bold text-center text-blue-400')
            try:
                if system_stats['core_temps'] != None:
                    for idx, t in enumerate(system_stats['core_temps']):
                        ui.label().bind_text_from(system_stats, 'core_temps', backward=lambda stats, idx=idx, t=t: f"{t.label}: {stats[idx].current:.1f}°C")
                elif system_stats['temps']:
                    for label, sensors in system_stats['temps'].items():
                        for idx, t in enumerate(sensors):
                            ui.label().bind_text_from(system_stats, 'temps', backward=lambda stats, label=label, idx=idx, t=t: f"{label} {t.label}: {stats[label][idx].current:.1f}°C")
                else:
                    ui.label("Temperature data not available")
            except Exception as e:
                ui.label(f"Temperature sensors unavailable {e}").classes('text-xs')

async def system_stats_polling():
    global system_stats
    while True:
        sys = {
            'cpu_percent': psutil.cpu_percent(percpu=False),
            'core_percents': psutil.cpu_percent(percpu=True),
            'mem_percent': psutil.virtual_memory().percent,
            'mem_used': psutil.virtual_memory().used,
            'swap_used': psutil.swap_memory().used,
            'disk': psutil.disk_usage('/'),
            'temps': psutil.sensors_temperatures(),
            'core_temps': None if system_stats['core_temps'] == None else system_stats['temps']["coretemp"]
        }
        for k, v in sys.items():
            system_stats[k] = v
        await asyncio.sleep(3)
