import csv
import json
from datetime import datetime
from pathlib import Path
from helpers.DataCollections import DataPoint, data_store
from helpers.GlobalEnums import AktionName, GraphStyles, TimeFrames, DataPresentation


class SaveLoad:
    csv_path = Path("data_points.csv")
    fieldNames = [
        "aktion_name",
        "said_yes",
        "candidate_name",
        "dptimestamp",
    ]

    @classmethod
    def verify_file(cls) -> bool:
        if not cls.csv_path.exists():
            with cls.csv_path.open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(cls.fieldNames)
            return False
        return True

    @classmethod
    def load_all_data(cls):
        if not cls.verify_file():
            return

        data_store.data_points.clear()

        with cls.csv_path.open("r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                aktion_name = AktionName[row["aktion_name"]]
                print(row)
                point = DataPoint(
                    aktion_name=aktion_name,
                    said_yes=row["said_yes"] == "True",
                    candidate_name=row["candidate_name"],
                    dptimestamp=datetime.fromisoformat(row["dptimestamp"]),
                )

                data_store.add_point(point)


    @classmethod
    def save_new_data(cls, new_stuff: list[DataPoint]):
        cls.verify_file()
        with cls.csv_path.open("a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            for point in new_stuff:
                writer.writerow([
                    point.aktion_name.name,
                    point.said_yes,
                    point.candidate_name,
                    point.dptimestamp.isoformat(),
                ])


class AppState:
    def __init__(self):
        self.json_path = Path("app_state_data.json")
        self.loaded_state: dict
        self.selected_aktion_name = AktionName.CUSTOMER_ACQUISITION
        self.selected_aktion_toggles: dict[AktionName, bool] = {
            aktion: False
            for aktion in AktionName
        }
        self.selected_graph_style = GraphStyles.Line
        self.selected_timeframe = TimeFrames.Days
        self.selected_presentation = DataPresentation.Both_Together

    def verify_file(self):
        if not self.json_path.exists():
            default_state = {
                "selected_aktion_name": AktionName.CUSTOMER_ACQUISITION.name,
                "selected_aktion_toggles": {
                    aktion.name: False
                    for aktion in AktionName
                },
                "selected_graph_style": GraphStyles.Line.name,
                "selected_timeframe": TimeFrames.Days.name,
                "selected_presentation": DataPresentation.Both_Together.name,
            }

            with self.json_path.open("w", encoding="utf-8") as json_file:
                json.dump(default_state, json_file, indent=4)

            return False
        return True

    def load(self):
        self.verify_file()

        with self.json_path.open("r", encoding="utf-8") as json_file:
            self.loaded_state = json.load(json_file)

        print(self.loaded_state)

        self.selected_aktion_name = AktionName[self.loaded_state["selected_aktion_name"]]

        self.selected_aktion_toggles = {
            AktionName[aktion_name]: value
            for aktion_name, value in self.loaded_state["selected_aktion_toggles"].items()
        }

        self.selected_graph_style = GraphStyles[self.loaded_state["selected_graph_style"]]
        self.selected_timeframe = TimeFrames[self.loaded_state["selected_timeframe"]]
        self.selected_presentation = DataPresentation[self.loaded_state["selected_presentation"]]

    def save(self):
        save_state = {
                "selected_aktion_name": self.selected_aktion_name.name,
                "selected_aktion_toggles": {
                    aktion.name: value
                    for aktion, value in self.selected_aktion_toggles.items()
                },
                "selected_graph_style": self.selected_graph_style.name,
                "selected_timeframe": self.selected_timeframe.name,
                "selected_presentation": self.selected_presentation.name,
            }

        with open(self.json_path, "w", encoding="utf-8") as json_file:
            json.dump(save_state, json_file, indent=4)
