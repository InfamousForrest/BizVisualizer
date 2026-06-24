import numpy as np
from kivy.app import App
from datetime import datetime
from matplotlib import pyplot as plt
from helpers.DataCollections import DataPoint
from helpers.GlobalEnums import AktionName, GraphStyles, TimeFrames, DataPresentation
from collections import defaultdict
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
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

    def get_time_bucket(self, timestamp: datetime):
        time_frame = App.get_running_app().app_state.selected_timeframe

        if time_frame == TimeFrames.Days:
            return timestamp.date()

        elif time_frame == TimeFrames.Weeks:
            year, week, day = timestamp.isocalendar()
            return f"{year}-w{week:02d}"

        elif time_frame == TimeFrames.Months:
            return timestamp.strftime("%y-%m")

        elif time_frame == TimeFrames.Years:
            return timestamp.year

        else:
            return timestamp.now()

    def build_timeframe_activity_counts(self):
        presentation = App.get_running_app().app_state.selected_presentation
        separate = presentation == DataPresentation.Both_Separate

        if separate:
            counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        else:
            counts = defaultdict(lambda: defaultdict(int))

        for graph_key, points in self.graph_points.items():
            aktion, yes_no = graph_key

            for point in points:
                bucket = self.get_time_bucket(point.dptimestamp)

                if separate:
                    counts[bucket][aktion][point.said_yes] += 1
                else:
                    counts[bucket][aktion] += 1

        return counts

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        self.border_line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )

    def plot_data(self, graph_points:  dict[tuple[AktionName, bool | None], list[DataPoint]]):
        self.graph_points = graph_points
        self.clear_widgets()

        if not self.graph_points:
            return

        counts = self.build_timeframe_activity_counts()
        self.draw_graph(counts)

    def get_all_aktions_from_counts(self, counts):
        aktions = set()

        for activity_counts in counts.values():
            for aktion in activity_counts.keys():
                aktions.add(aktion)

        return sorted(aktions, key=lambda a: a.name)

    def draw_graph(self, counts):
        app_state = App.get_running_app().app_state
        presentation = app_state.selected_presentation
        graph_style = app_state.selected_graph_style
        separate = presentation == DataPresentation.Both_Separate

        fig, ax = plt.subplots()
        aktions = self.get_all_aktions_from_counts(counts)
        buckets = sorted(counts.keys())
        x_positions = np.arange(len(buckets))

        if separate:
            for i, aktion in enumerate(aktions):
                yes_values = []
                no_values = []

                for bucket in buckets:
                    yes_values.append(counts[bucket][aktion].get(True, 0))
                    no_values.append(counts[bucket][aktion].get(False, 0))

                if graph_style == GraphStyles.Line:
                    ax.plot(buckets, yes_values, marker="o", label=f"{aktion.name} Yes")
                    ax.plot(buckets, no_values, marker="o", label=f"{aktion.name} No")

                elif graph_style == GraphStyles.Bar:
                    bar_width = 0.8 / len(aktions)
                    offset = (i - len(aktions) / 2) * bar_width + bar_width / 2
                    bar_x = x_positions + offset

                    ax.bar(bar_x, no_values, label=f"{aktion.name} No")
                    ax.bar(bar_x, yes_values, bottom=no_values, label=f"{aktion.name} Yes")

            if graph_style == GraphStyles.Bar:
                ax.set_xticks(x_positions)
                ax.set_xticklabels(buckets)

        else:
            for i, aktion in enumerate(aktions):
                values = []

                for bucket in buckets:
                    values.append(counts[bucket].get(aktion, 0))

                if graph_style == GraphStyles.Line:
                    ax.plot(buckets, values, marker="o", label=aktion.name)

                elif graph_style == GraphStyles.Bar:
                    bar_width = 0.8 / len(aktions)
                    offset = (i - len(aktions) / 2) * bar_width + bar_width / 2
                    bar_x = x_positions + offset

                    ax.bar(bar_x, values, width=bar_width, label=aktion.name)

            if graph_style == GraphStyles.Bar:
                ax.set_xticks(x_positions)
                ax.set_xticklabels(buckets)

        ax.set_title("Activity Counts Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Count")
        ax.legend()
        ax.grid(True)

        fig.autofmt_xdate()

        self.add_widget(FigureCanvasKivyAgg(fig))
