from pathlib import Path

from data.db import Database
from .common import read_csv, clean, to_float, to_int


def load_payment_options(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "request_payment_options.csv")

    query = """
        INSERT OR REPLACE INTO request_payment_options (
            payment_option_id,
            request_id,
            payment_method,
            payment_amount,
            number_of_payments,
            first_payment_date,
            payment_frequency_days,
            financing_fee,
            total_payable_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = [
        (
            clean(row["payment_option_id"]),
            clean(row["request_id"]),
            clean(row["payment_method"]),
            to_float(row["payment_amount"]),
            to_int(row["number_of_payments"]),
            clean(row["first_payment_date"]),
            to_int(row["payment_frequency_days"]),
            to_float(row["financing_fee"]),
            to_float(row["total_payable_amount"]),
        )
        for row in rows
    ]

    result = db.executemany(query, values)
    print(result.rowcount, "payment options loaded")