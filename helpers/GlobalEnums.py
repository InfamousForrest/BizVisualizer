from enum import Enum


class AktionName(Enum):
    CUSTOMER_ACQUISITION = ("New Customer", (0.2, 0.9, 0.3, 1))
    MPA_INPERSON = ("MPA - In Person", (1, 0.6, 0.1, 1))
    MPA_PHONE = ("MPA - Phone", (0.7, 0.1, 0.2, 1))
    DTM_INPERSON = ("DTM - In Person", (0.4, 0.1, 0.9, 1))
    DTM_PHONE = ("DTM - Phone", (0.8, 0.8, 0.1, 1))
    QUALIFYINGCALL = ("Qualifying Call", (0, 0.5, 0.7, 1))
    QI1 = ("QI1", (0.7, 0.7, 0.4, 1))

    def __init__(self, label: str, color: tuple[float, float, float, float]):
        self.label = label
        self.color = color


class GraphStyles(Enum):
    Line = "Line Graph"
    Bar = "Bar Chart"


class TimeFrames(Enum):
    Days = "Days"
    Weeks = "Weeks"
    Months = "Months"
    Years = "Years"


class DataPresentation(Enum):
    Positives = "Positive Responses"
    Negatives = "Negative Responses"
    Both_Separate = "Both - Separate"
    Both_Together = "Both - Together"
