from nicegui import ui

async def styles():

    ui.colors(
        primary="#9EDFEC",
        secondary="#274c77",
        accent="#fac529",
        dark="#292e32",  # dark='#171614',
        dark_page="#212428",  # dark_page='#191e21',
        positive="#255238",
        negative="#2c0e37",
        info="#586469",
        warning="#BF5234",
        header = '#788391'
    )

style_vars = {
    'flex-shadow': '0px_1px_5px_rgba(0,0,0,0.2),_0px_2px_2px_rgba(0,0,0,0.14),_0px_3px_1px_-2px_rgba(0,0,0,0.12)'
}