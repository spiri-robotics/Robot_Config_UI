from nicegui import ui
import inspect

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
        result = False
        if self.state:
            if inspect.iscoroutinefunction(self.on_switch):
                result = await self.on_switch()
            else:
                result = self.on_switch()
        else:
            if inspect.iscoroutinefunction(self.off_switch):
                result = await self.off_switch()
            else:
                result = self.off_switch()
        if result:
            self.state = not self.state
            self.update()

    def update(self) -> None:
        self.color = self.on_color if self.state else self.off_color
        label = self.on_label if self.state else self.off_label
        self.props(f"color={self.color}")
        self.set_text(label)
        super().update()