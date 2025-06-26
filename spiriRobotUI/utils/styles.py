from nicegui import ui

DARK_MODE = True

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
    )
    ui.html(
        """
        <style>
        @media (prefers-color-scheme: dark) {
            .dark-card {
                box-shadow: 0px 4px 12px rgba(0,0,0,0.8) !important;
            }
            .nicegui-markdown p,
            .nicegui-markdown li {
                font-size: 14px !important;
                line-height: 1.3 !important;
                margin-bottom: 4px !important;
            }
            .nicegui-markdown h1 {
                font-size: 24px !important;
                font-weight: bold !important;
            }
            .nicegui-markdown h2 {
                font-size: 20px !important;
                font-weight: bold !important;
            }
            .nicegui-markdown h3 {
                font-size: 18px !important;
                font-weight: bold !important;
            }
            .nicegui-markdown h4,
            .nicegui-markdown h5,
            .nicegui-markdown h6 {
                font-size: 16px !important;
                font-weight: bold !important;
            }
        }
        </style>
        """
    )
