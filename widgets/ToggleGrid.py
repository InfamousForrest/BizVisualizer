from typing import Callable
from widgets.LabeledToggle import LabeledToggle
from helpers.GlobalEnums import AktionName
from kivy.uix.gridlayout import GridLayout


class ToggleGrid(GridLayout):
    def __init__(self, on_change: Callable[[bool], None] | None = None, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        self.size_hint_y = None
        self.height = 180
        self.spacing = 1
        self.padding = 1

        self.toggles: dict[AktionName, LabeledToggle] = {}

        for aktion_name in AktionName:
            toggle = LabeledToggle(
                aktion_name=aktion_name.label,
                active_color=aktion_name.color,
                on_change=on_change,
            )

            self.add_widget(toggle)
            self.toggles[aktion_name] = toggle

    def get_active_aktions(self) -> list[AktionName]:
        return [
            aktion_name
            for aktion_name, toggle in self.toggles.items()
            if toggle.is_active
        ]

    def is_aktion_active(self, aktion_name: AktionName) -> bool:
        return self.toggles[aktion_name].is_active
