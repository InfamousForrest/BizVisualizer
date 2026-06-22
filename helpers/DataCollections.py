from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from helpers.GlobalEnums import AktionName, DataPresentation


@dataclass
class DataPoint:
    aktion_name: AktionName
    said_yes: bool
    candidate_name: str
    timestamp: datetime


class GraphSet:
    def __init__(self):
        self.true_points: list[DataPoint] = []
        self.false_points: list[DataPoint] = []

    def add_point(self, point: DataPoint):
        if point.said_yes:
            self.true_points.append(point)
        else:
            self.false_points.append(point)

    def get_point_set(self, which: bool) -> list[DataPoint]:
        if which:
            return self.true_points
        else:
            return self.false_points

    def get_all_points(self) -> list[DataPoint]:
        return self.true_points + self.false_points


class DataStore:
    def __init__(self):
        self.data_points: dict[AktionName, GraphSet] = {}

    def add_point(self, point: DataPoint):
        self.data_points[point.aktion_name].add_point(point)

    def add_point(self, aktion_name: AktionName, said_yes: bool, candidate_name: str):
        self.data_points[aktion_name].add_point(
            DataPoint(
                aktion_name=aktion_name,
                said_yes=said_yes,
                candidate_name=candidate_name,
                timestamp=datetime.now(),
            )
        )

    def get_points_for_aktions(self, aktions, presentation: DataPresentation):
        points: dict[tuple[AktionName, bool | None], list[DataPoint]] = {}
        for aktion in aktions:
            if presentation == DataPresentation.Positives:
                points[(aktion, True)] = self.data_points[aktion].get_point_set(which=True)
            elif presentation == DataPresentation.Negatives:
                points[(aktion, False)] = self.data_points[aktion].get_point_set(which=False)
            elif presentation == DataPresentation.Both_Together:
                points[(aktion, None)] = self.data_points[aktion].get_all_points()
            elif presentation == DataPresentation.Both_Separate:
                points[(aktion, True)] = self.data_points[aktion].get_point_set(which=True)
                points[(aktion, False)] = self.data_points[aktion].get_point_set(which=False)

        return points

    def get_all_points(self):
        return self.data_points


data_store = DataStore()
