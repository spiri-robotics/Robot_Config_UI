from nicegui import ui

async def styles():

    ui.colors(
        primary="#9EDFEC",
        secondary="#274c77",
        accent="#c52e6d",
        dark="#292e32",  # dark='#171614',
        dark_page="#212428",  # dark_page='#191e21',
        positive="#609926",
        negative="#BF5234",
        info="#586469",
        warning="#fac529",
        exited="#811D1D",
        restarting="#77400D",
        running="#609926", 
        created="#818307", 
        paused="#0e1977", 
        dead="#000000",
        header = '#788391'
    )

style_vars = {
    'flex-shadow': '0px_1px_5px_rgba(0,0,0,0.2),_0px_2px_2px_rgba(0,0,0,0.14),_0px_3px_1px_-2px_rgba(0,0,0,0.12)'
}