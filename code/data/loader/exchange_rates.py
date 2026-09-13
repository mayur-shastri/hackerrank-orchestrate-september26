from pathlib import Path

from data.db import Database
from .common import read_csv, clean, to_float


def load_exchange_rates(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "exchange_rates.csv")

    query = """
        INSERT OR REPLACE INTO exchange_rates (
            rate_date,
            from_currency,
            to_currency,
            rate
        )
        VALUES (?, ?, ?, ?)
    """

    values = [
        (
            clean(row["rate_date"]),
            clean(row["from_currency"]),
            clean(row["to_currency"]),
            to_float(row["rate"]),
        )
        for row in rows
    ]

    result = db.executemany(query, values)
    print(result.rowcount, "exchange rates loaded")