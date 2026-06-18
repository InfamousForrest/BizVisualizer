from helpers.GlobalEnums import *
from helpers.DataCollections import data_store
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from datetime import datetime
from kivy.uix.image import Image


class ImageButton(Button):
    def __init__(self, image_source, button_color, **kwargs):
        super().__init__(**kwargs)

        self.text = ""
        self.background_normal = ""
        self.background_color = button_color

        self.icon = Image(
            source=image_source,
            size_hint=(None, None),
            size=(80, 80),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.add_widget(self.icon)

        self.bind(pos=self.update_icon_position, size=self.update_icon_position)

    def update_icon_position(self, *args):
        self.icon.center = self.center


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        self.selected_action = AktionName.QI1
        self.yes_or_no = True
        self.yes_image = "assets/PNGs/ThumbsUp.png"
        self.no_image = "assets/PNGs/ThumbsDown.png"
        self.sales_image = "assets/PNGs/Sales.png"
        self.sampling_image = "assets/PNGs/Sampling.png"
        self.write_image = "assets/PNGs/Pencil.png"

        self.button_row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=100
        )

        self.yes_button = ImageButton(
            image_source=self.get_ybutton_icons(),
            button_color=(0.1, 0.7, 0.2, 1),
            size_hint=(1, 1),
        )

        self.no_button = ImageButton(
            image_source=self.get_nbutton_icons(),
            button_color=(0.7, 0.1, 0.2, 1),
            size_hint=(1, 1),
        )

        self.name_input = TextInput(
            hint_text="Their Name",
            multiline=False,
            halign="center",
            font_size=32,
            size_hint_y=None,
            height=80,
        )

        self.action_dropdown = Spinner(
            text=AktionName.QI1.label,
            values=[action.label for action in AktionName],
            font_size=28,
            size_hint_y=None,
            height=80,
        )

        self.output = TextInput(
            text="Saved data will appear here",
            readonly=True,
            font_size=24,
        )

        self.action_dropdown.bind(text=self.on_action_changed)
        self.yes_button.bind(on_press=lambda button: self.record_data(True))
        self.no_button.bind(on_press=lambda button: self.record_data(False))
        self.button_row.add_widget(self.yes_button)
        self.button_row.add_widget(self.no_button)

        self.add_widget(self.action_dropdown)
        self.add_widget(self.button_row)
        self.add_widget(self.name_input)
        self.add_widget(self.output)

    def get_ybutton_icons(self):
        if self.selected_action == AktionName.CUSTOMER_ACQUISITION:
            return self.sales_image

        return self.yes_image

    def get_nbutton_icons(self):
        if self.selected_action == AktionName.CUSTOMER_ACQUISITION:
            return self.sampling_image

        return self.no_image

    def update_buttons(self):
        self.yes_button.icon.source = self.get_ybutton_icons()
        self.no_button.icon.source = self.get_nbutton_icons()
        ca = (0.8, 0.1, 0.1, 1)
        cb = (0.1, 0.8, 0.7, 1)

        self.yes_button.icon.reload()
        self.no_button.icon.reload()

        self.yes_button.background_color = (0.1, 0.7, 0.2, 1)

        if self.selected_action == AktionName.CUSTOMER_ACQUISITION:
            self.no_button.background_color = cb
        else:
            self.no_button.background_color = ca

    def record_data(self, answer):
        name = self.name_input.text.strip().replace(",", "")
        timestamp = datetime.utcnow().isoformat()
        #timestamp = datetime.now(datetime.UTC).isoformat()

        line = f"{self.selected_action.label},{answer},{timestamp},{name}\n"
        self.output.text += "\n" + line
        self.name_input.text = ""

        data_store.add_point(
            aktion_name=self.selected_action,
            said_yes=answer,
            candidate_name=name,
        )

    def on_action_changed(self, spinner, selected_text):
        self.selected_action = next(
            action for action in AktionName
            if action.label == selected_text
        )

        self.update_buttons()


class TrackerApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    TrackerApp().run()
