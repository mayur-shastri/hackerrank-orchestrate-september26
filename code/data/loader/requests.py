from pathlib import Path

from data.db import Database
from .common import read_csv, clean, to_float, to_bool


def load_requests(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "requests.csv")

    query = """
        INSERT OR REPLACE INTO requests (
            request_id,
            user_id,
            request_date,
            request_type,
            requested_amount,
            desired_completion_date,
            allows_partial_payment,
            request_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = [
        (
            clean(row["request_id"]),
            clean(row["user_id"]),
            clean(row["request_date"]),
            clean(row["request_type"]),
            to_float(row["requested_amount"]),
            clean(row["desired_completion_date"]),
            to_bool(row["allows_partial_payment"]),
            clean(row["request_text"]),
        )
        for row in rows
    ]

    result = db.executemany(query, values)
    print(result)