from pathlib import Path

from data.db import Database
from .common import read_csv, clean, to_float, to_int, to_json


def load_financial_profiles(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "financial_profiles.csv")

    query = """
        INSERT OR REPLACE INTO financial_profiles (
            user_id,
            home_currency,
            current_available_balance,
            minimum_balance_to_keep,
            financial_priorities,
            expense_categories_to_protect,
            expense_categories_user_is_willing_to_reduce,
            expense_categories_user_is_willing_to_stop,
            payment_methods_user_will_consider,
            max_installment_months
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = [
        (
            clean(row["user_id"]),
            clean(row["home_currency"]),
            to_float(row["current_available_balance"]),
            to_float(row["minimum_balance_to_keep"]),
            to_json(row["financial_priorities"]),
            to_json(row["expense_categories_to_protect"]),
            to_json(row["expense_categories_user_is_willing_to_reduce"]),
            to_json(row["expense_categories_user_is_willing_to_stop"]),
            to_json(row["payment_methods_user_will_consider"]),
            to_int(row["max_installment_months"]),
        )
        for row in rows
    ]

    result = db.executemany(query, values)
    print(result)