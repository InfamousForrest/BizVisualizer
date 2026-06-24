from __future__ import annotations
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


LOCAL_TIMEZONE = ZoneInfo("America/New_York")


@dataclass
class ActivityRow:
    timestamp_utc: datetime
    timestamp_local: datetime
    raw_data: dict[str, str]


def parse_timestamp(timestamp_text: str) -> tuple[datetime, datetime]:
    """
    Converts an ISO timestamp string into:
    - UTC/offset-aware datetime
    - local datetime for display/graphing
    """

    timestamp_text = timestamp_text.strip()

    # Handles ISO strings like:
    # 2026-06-07T08:35:00+00:00
    # 2026-06-07T08:35:00.0000000+00:00
    timestamp_utc = datetime.fromisoformat(timestamp_text)

    if timestamp_utc.tzinfo is None:
        raise ValueError(f"Timestamp has no timezone info: {timestamp_text}")

    timestamp_local = timestamp_utc.astimezone(LOCAL_TIMEZONE)

    return timestamp_utc, timestamp_local


def read_activity_csv(csv_path: str | Path, timestamp_column: str = "timestamp") -> list[ActivityRow]:
    """
    Reads one CSV file and parses its timestamp column.
    """

    csv_path = Path(csv_path)
    rows: list[ActivityRow] = []

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if timestamp_column not in reader.fieldnames:
            raise KeyError(
                f"CSV is missing timestamp column '{timestamp_column}'. "
                f"Found columns: {reader.fieldnames}"
            )

        for row in reader:
            timestamp_utc, timestamp_local = parse_timestamp(row[timestamp_column])

            rows.append(
                ActivityRow(
                    timestamp_utc=timestamp_utc,
                    timestamp_local=timestamp_local,
                    raw_data=row,
                )
            )

    return rows


def read_activity_folder(folder_path: str | Path, timestamp_column: str = "timestamp") -> list[ActivityRow]:
    """
    Reads every .csv file in a folder.
    """

    folder_path = Path(folder_path)
    all_rows: list[ActivityRow] = []

    for csv_file in folder_path.glob("*.csv"):
        all_rows.extend(read_activity_csv(csv_file, timestamp_column))

    return sorted(all_rows, key=lambda row: row.timestamp_utc)