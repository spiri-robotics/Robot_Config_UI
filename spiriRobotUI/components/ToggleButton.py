from nicegui import ui

class ToggleButton(ui.button):
    def __init__(
        self,
        *args,
        on_label="on",
        off_label="off",
        on_switch=None,
        off_switch=None,
        state,
        on_color="positive",
        off_color="warning",
        **kwargs,
    ):
        
        super().__init__(*args, **kwargs)
        self.state = state
        self.on_color = on_color
        self.off_color = off_color
        self.color = self.off_color
        self.on_label = on_label
        self.off_label = off_label
        self.on_switch = on_switch
        self.off_switch = off_switch
        self.on("click", self.toggle)

    async def toggle(self) -> None:
        if self.state:
            self.on_switch()
        elif not self.state:
            self.off_switch()
        self.state = not self.state
        self.update()

    def update(self) -> None:
        self.color = self.on_color if self.state else self.off_color
        label = self.on_label if self.state else self.off_label
        self.props(f"color={self.color}")
        self.set_text(label)
        super().update()