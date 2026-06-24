from widgets.ToggleGrid import ToggleGrid
from widgets.GraphWindow import GraphBox
from helpers.GlobalEnums import GraphStyles, TimeFrames, DataPresentation, AktionName
from helpers.DataCollections import data_store, DataPoint
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout


class GraphScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        self.current_graph: dict[tuple[AktionName, bool | None], list[DataPoint]] = {}

        self.dropdown_row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=100
        )

        self.graph_type_dropdown = Spinner(
            text=App.get_running_app().app_state.selected_graph_style.value,
            values=[action.value for action in GraphStyles],
            font_size=28,
            size_hint_y=None,
            height=80,
        )

        self.timeframe_dropdown = Spinner(
            text=App.get_running_app().app_state.selected_timeframe.value,
            values=[action.value for action in TimeFrames],
            font_size=28,
            size_hint_y=None,
            height=80,
        )

        self.presentation_dropdown = Spinner(
            text=App.get_running_app().app_state.selected_presentation.value,
            values=[action.value for action in DataPresentation],
            font_size=28,
            size_hint_y=None,
            height=80,
        )

        self.toggle_grid = ToggleGrid(
            on_change=self.refresh_graph,
        )

        self.dropdown_row.add_widget(self.graph_type_dropdown)
        self.dropdown_row.add_widget(self.timeframe_dropdown)
        self.dropdown_row.add_widget(self.presentation_dropdown)

        self.add_widget(self.dropdown_row)
        self.add_widget(self.toggle_grid)
        self.graph_box = GraphBox()
        self.add_widget(self.graph_box)

        self.graph_type_dropdown.bind(text=lambda *_: self.on_graph_style_changed())
        self.timeframe_dropdown.bind(text=lambda *_: self.on_timeframe_changed())
        self.presentation_dropdown.bind(text=lambda *_: self.on_graph_presentation())

    def refresh_graph(self, *args):
        active_aktions = self.toggle_grid.get_active_aktions()
        presentation = self.get_selected_presentation()
        self.current_graph = data_store.get_points_for_aktions(active_aktions, presentation)
        self.graph_box.plot_data(self.current_graph)

    def get_selected_graph_type(self) -> GraphStyles:
        return GraphStyles(self.graph_type_dropdown.text)

    def on_graph_style_changed(self):
        App.get_running_app().app_state.selected_graph_style = self.get_selected_graph_type()
        self.refresh_graph()

    def get_selected_timeframe(self) -> TimeFrames:
        return TimeFrames(self.timeframe_dropdown.text)

    def on_timeframe_changed(self):
        App.get_running_app().app_state.selected_timeframe = self.get_selected_timeframe()
        self.refresh_graph()

    def get_selected_presentation(self) -> DataPresentation:
        return DataPresentation(self.presentation_dropdown.text)

    def on_graph_presentation(self):
        App.get_running_app().app_state.selected_presentation = self.get_selected_presentation()
        self.refresh_graph()


class GrapherApp(App):
    def build(self):
        return GraphScreen()


if __name__ == "__main__":
    GrapherApp().run()
