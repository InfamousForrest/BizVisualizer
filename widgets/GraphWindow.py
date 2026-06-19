from helpers.DataCollections import data_store, DataPoint
from helpers.GlobalEnums import AktionName, GraphStyles
from collections import Counter
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from matplotlib.figure import Figure
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class GraphBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.graph_points: dict[tuple[AktionName, bool | None], list[DataPoint]] = {}
        self.orientation = "vertical"
        self.size_hint_y = 1
        self.padding = 12

        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

            Color(0.45, 0.45, 0.45, 1)
            self.border_line = Line(
                rectangle=(self.x, self.y, self.width, self.height),
                width=2
            )

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        self.border_line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )

    def plot_data(self, data_points, graph_type):
        self.graph_points = data_points
        self.selected_graph_style = graph_type
        self.redraw_graph()

    def redraw_graph(self):
        self.clear_widgets()

        if not self.graph_points:
            return

        if self.selected_graph_style == GraphStyles.Bar:
            self.draw_bar_graph()

        elif self.selected_graph_style == GraphStyles.Line:
            self.draw_line_graph()

    def draw_bar_graph(self):
        counts = Counter(
            point.aktion_name.name
            for point in self.graph_points
        )

        fig = Figure()
        ax = fig.add_subplot(111)

        names = list(counts.keys())
        values = list(counts.values())

        ax.bar(names, values)
        ax.set_title("Actions Recorded")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=30)

        #fig.tight_layout()
        fig.subplots_adjust(bottom=0.25)

        self.canvas_widget = FigureCanvasKivyAgg(fig)
        self.add_widget(self.canvas_widget)

    def draw_line_graph(self):
        counts = Counter(
            point.timestamp.strftime("%Y-%m-%d")
            for point in self.data_points
        )

        dates = sorted(counts.keys())
        values = [counts[date] for date in dates]

        fig = Figure()
        ax = fig.add_subplot(111)

        ax.plot(dates, values, marker="o")
        ax.set_title("Actions Over Time")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=30)

        #fig.tight_layout()
        fig.subplots_adjust(bottom=0.25)

        self.canvas_widget = FigureCanvasKivyAgg(fig)
        self.add_widget(self.canvas_widget)
