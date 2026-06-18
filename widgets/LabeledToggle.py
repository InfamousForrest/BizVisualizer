from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


class LabeledToggle(BoxLayout):
    def __init__(self, aktion_name, active_color, on_change=None, **kwargs):
        super().__init__(**kwargs)

        self.aktion_name = aktion_name
        self.active_color = active_color
        self.inactive_color = (0.45, 0.45, 0.45, 1)
        self.on_change = on_change

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = 56
        self.spacing = 8

        self.checkbox = CheckBox(
            active=False,
            size_hint_x=None,
            width=56,
        )

        self.label = Label(
            text=aktion_name,
            halign="left",
            valign="middle",
            color=self.inactive_color,
        )

        self.label.bind(size=self.label.setter("text_size"))

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

        self.checkbox.bind(active=self._on_checkbox_changed)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.checkbox.active = not self.checkbox.active
            return True

        return super().on_touch_down(touch)

    def _on_checkbox_changed(self, checkbox, active):
        self.refresh_visual_state()

        if self.on_change:
            self.on_change(self.aktion_name, active)

    def refresh_visual_state(self):
        self.label.color = (
            self.active_color
            if self.checkbox.active
            else self.inactive_color
        )

    @property
    def is_active(self) -> bool:
        return self.checkbox.active

    def set_active(self, value: bool):
        self.checkbox.active = value
        self.refresh_visual_state()
