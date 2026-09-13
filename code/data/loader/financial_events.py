from pathlib import Path

from data.db import Database
from .common import read_csv, clean, to_float


def load_financial_events(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "financial_events.csv")

    query = """
        INSERT OR REPLACE INTO financial_events (
            event_id,
            user_id,
            event_type,
            description,
            category,
            direction,
            amount,
            currency,
            event_date,
            settlement_date,
            status,
            linked_event_id,
            flexibility,
            minimum_allowed_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = [
        (
            clean(row["event_id"]),
            clean(row["user_id"]),
            clean(row["event_type"]),
            clean(row["description"]),
            clean(row["category"]),
            clean(row["direction"]),
            to_float(row["amount"]),
            clean(row["currency"]),
            clean(row["event_date"]),
            clean(row["settlement_date"]),
            clean(row["status"]),
            clean(row["linked_event_id"]),
            clean(row["flexibility"]),
            to_float(row["minimum_allowed_amount"]),
        )
        for row in rows
    ]

    db.executemany(query, values)