from helpers.GlobalEnums import AktionName
from helpers.DataCollections import DataPoint, data_store
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from datetime import datetime
from kivy.uix.image import Image
from helpers.SaveLoad import SaveLoad


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


class RecScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        self.app_state = App.get_running_app().app_state
        self.saveload = SaveLoad

        self.new_data: list[DataPoint] = []
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

        self.button_row2 = BoxLayout(
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

        icon, color = self.get_nbutton_icons()

        self.no_button = ImageButton(
            image_source=icon,
            button_color=color,
            size_hint=(1, 1),
        )

        self.undo_button = Button(
            text="UNDO",
            font_size=24,
            size_hint_y=None,
            height=100,
        )

        self.clear_button = Button(
            text="CLEAR",
            font_size=24,
            size_hint_y=None,
            height=100,
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
            text=self.app_state.selected_aktion_name.label,
            values=[action.label for action in AktionName],
            font_size=28,
            size_hint_y=None,
            height=80,
        )

        self.output = TextInput(
            hint_text="Saved data will appear here",
            readonly=True,
            font_size=24,
        )

        self.undo_button.bind(on_press=self.delete_last_point)
        self.clear_button.bind(on_press=self.clear_new_data)
        self.action_dropdown.bind(text=self.on_action_changed)
        self.yes_button.bind(on_press=lambda button: self.record_data(True))
        self.no_button.bind(on_press=lambda button: self.record_data(False))
        self.button_row.add_widget(self.yes_button)
        self.button_row.add_widget(self.no_button)
        self.button_row2.add_widget(self.undo_button)
        self.button_row2.add_widget(self.clear_button)

        self.add_widget(self.action_dropdown)
        self.add_widget(self.button_row)
        self.add_widget(self.name_input)
        self.add_widget(self.output)
        self.add_widget(self.button_row2)

    def get_ybutton_icons(self):
        if self.app_state.selected_aktion_name == AktionName.CUSTOMER_ACQUISITION:
            return self.sales_image

        return self.yes_image

    def get_nbutton_icons(self):
        if self.app_state.selected_aktion_name == AktionName.CUSTOMER_ACQUISITION:
            return self.sampling_image, (0.1, 0.8, 0.7, 1)

        return self.no_image, (0.8, 0.1, 0.1, 1)

    def update_buttons(self):
        self.yes_button.icon.source = self.get_ybutton_icons()
        icon, color = self.get_nbutton_icons()
        self.no_button.icon.source = icon

        self.yes_button.icon.reload()
        self.no_button.icon.reload()

        self.yes_button.background_color = (0.1, 0.7, 0.2, 1)
        self.no_button.background_color = color

    def record_data(self, answer):
        self.new_data.append(
            DataPoint(
                aktion_name=self.app_state.selected_aktion_name,
                said_yes=answer,
                candidate_name=self.name_input.text.strip().replace(",", ""),
                dptimestamp=datetime.utcnow()
            )
        )

        self.name_input.text = ""
        self.display_records()

    def display_records(self):
        self.output.text = ""

        if len(self.new_data) == 0:
            return
        print(len(self.new_data))
        for data in self.new_data:
            line = f"{data.candidate_name},{data.aktion_name.label},{data.said_yes},{data.dptimestamp.isoformat()}\n"
            self.output.text += "\n" + line

    def on_action_changed(self, spinner, selected_text):
        self.app_state.selected_aktion_name = next(
            action for action in AktionName
            if action.label == selected_text
        )

        self.update_buttons()

    def delete_last_point(self, instance):
        if len(self.new_data) > 0:
            self.new_data.pop()
            self.display_records()

    def clear_new_data(self, instance):
        if len(self.new_data) > 0:
            self.new_data.clear()
            self.display_records()

    def commit_data(self):
        print(len(self.new_data))
        data_store.add_points(self.new_data)
        self.saveload.save_new_data(self.new_data)
        self.clear_new_data(instance=self)


class TrackerApp(App):
    def build(self):
        return RecScreen()


if __name__ == "__main__":
    TrackerApp().run()
