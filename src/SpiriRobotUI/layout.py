from contextlib import contextmanager
from nicegui import ui
from SpiriRobotUI import extension_loader
from loguru import logger
from SpiriRobotUI.extension_loader import ExtensionLoader

style_vars = {
    "flex-shadow": "0px_1px_5px_rgba(0,0,0,0.2),_0px_2px_2px_rgba(0,0,0,0.14),_0px_3px_1px_-2px_rgba(0,0,0,0.12)",
    "half": "calc(50%-(var(--nicegui-default-gap)/2))",
    "third": "calc((100%/3)-(var(--nicegui-default-gap)/1.5))",
    "fourth": "calc(25%-(var(--nicegui-default-gap)/(4/3)))"
}

def draw_sidebar_items():
    """Create menu buttons for navigation."""
    extension_loader = ExtensionLoader()
    for extension in extension_loader.extension_registry:
        extension_loader.extension_registry[extension].extension.draw_sidebar_item()

@contextmanager
def frame(nav_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""

    ui.colors(
        primary="#274c77",
        secondary="#9EDFEC",
        accent="#89BEC9",
        dark="#292e32",
        dark_page="#212428",
        positive="#609926",
        negative="#BF5234",
        info="#9E9E9E",
        warning="#fac529",
        exited="#811D1D",
        restarting="#77400D",
        running="#609926", 
        created="#818307", 
        paused="#0e1977", 
        dead="#000000"
    )

    # Sidebar
    with ui.left_drawer(value=True).props("width=300 breakpoint=200 bordered"):
        with ui.column().classes("w-full p-2"):
            with ui.row(align_items='center').classes("w-full justify-between pb-2"):
                ui.image("SpiriRobotUI/icons/Spiri_logo_Mixed_dual_background.svg").classes("h-16 w-16")
                ui.label("Spiri Robot UI").classes("text-2xl font-semibold")
            with ui.scroll_area().classes("w-full"):
                draw_sidebar_items()
    
    # Header
    with ui.row(align_items="end"):
        ui.button(icon="account_circle", color="info").props("flat fab").classes("absolute top-7 right-4")
        ui.button(icon="more_vert", color="info").props("flat fab").classes("absolute top-7 right-16")
        ui.markdown("## Plug-in Coordinator")
    with ui.row(align_items="end").classes("w-full justify-between"):
        ui.label("Your favourite plugins, now all in one place.").classes("text-xl text-info")

    ui.separator()

    with ui.column().classes("absolute-center items-center"):
        yield

