import csv
from datetime import datetime
from pathlib import Path
from helpers.DataCollections import GraphSet
from helpers.GlobalEnums import AktionName


class DataStorage:
    def __init__(self, csv_path: str = "data_points.csv"):
        self.csv_path = Path(csv_path)
        self.data_points: dict[AktionName, GraphSet] = {}