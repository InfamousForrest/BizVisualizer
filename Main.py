from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from RecorderScreen import RecScreen
from VisualizerScreen import GraphScreen
from helpers.SaveLoad import AppState


class MainTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.do_default_tab = False
        self.tab_width = None
        self.tab_pos = "top_mid"

        self.record_tab = TabbedPanelItem(text="Record")
        self.record_tab.add_widget(RecScreen())

        self.graph_tab = TabbedPanelItem(text="Graphs")
        self.graph_tab.add_widget(GraphScreen())

        self.add_widget(self.record_tab)
        self.add_widget(self.graph_tab)

        self.default_tab = self.record_tab

        self.bind(width=self.resize_tabs)

    def resize_tabs(self, *args):
        tabs = [self.record_tab, self.graph_tab]

        tab_width = self.width / len(tabs)

        for tab in tabs:
            tab.size_hint_x = None
            tab.width = tab_width


class MyApp(App):
    def build(self):
        self.app_state = AppState()
        Window.bind(on_keyboard=self.on_keyboard)
        return MainTabs()

    def on_stop(self):
        self.app_state.save()
        return False

    def on_start(self):
        self.app_state.load()

    def on_quit(self):
        self.app_state.save()
        return False

    def on_close(self):
        self.app_state.save()
        return False

    def on_pause(self):
        self.app_state.save()
        return True

    def on_keyboard(self, window, key, *args):
        if key == 27:
            self.app_state.save()
            return False
        return True

MyApp().run()