from kivy.app import App
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from RecorderScreen import RecScreen
from VisualizerScreen import GraphScreen
from helpers.SaveLoad import AppState, SaveLoad


class MainTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.record_screen = RecScreen()
        self.graph_screen = GraphScreen()

        self.do_default_tab = False
        self.tab_width = None
        self.tab_pos = "top_mid"

        self.record_tab = TabbedPanelItem(text="Record")
        self.record_tab.add_widget(self.record_screen)

        self.graph_tab = TabbedPanelItem(text="Graphs")
        self.graph_tab.add_widget(self.graph_screen)

        self.add_widget(self.record_tab)
        self.add_widget(self.graph_tab)

        self.default_tab = self.record_tab

        self.bind(current_tab=self.on_tab_switch)
        self.bind(width=self.resize_tabs)

    def on_tab_switch(self, instance, tab):
        if tab == self.graph_tab:
            print("Switched to Graphs")
            print(len(self.record_screen.new_data))
            self.record_screen.commit_data()
            self.graph_screen.refresh_graph()

        elif tab == self.record_tab:
            print("Switched to Record")

    def resize_tabs(self, *args):
        tabs = [self.record_tab, self.graph_tab]

        tab_width = self.width / len(tabs)

        for tab in tabs:
            tab.size_hint_x = None
            tab.width = tab_width


class MyApp(App):
    def build(self):
        self.app_state = AppState()
        self.app_state.load()
        self.main_tabs = MainTabs()
        self.saveload = SaveLoad()
        self.saveload.load_all_data()

        Window.bind(on_keyboard=self.on_keyboard)
        return self.main_tabs

    def on_stop(self):
        self.app_state.save()
        self.main_tabs.record_screen.commit_data()
        return False

    def on_quit(self):
        self.app_state.save()
        self.main_tabs.record_screen.commit_data()
        return False

    def on_close(self):
        self.app_state.save()
        self.main_tabs.record_screen.commit_data()
        return False

    def on_pause(self):
        self.app_state.save()
        self.main_tabs.record_screen.commit_data()
        return True

    def on_keyboard(self, window, key, *args):
        if key == 27:
            self.app_state.save()
            self.main_tabs.record_screen.commit_data()
            return False
        return True


MyApp().run()
