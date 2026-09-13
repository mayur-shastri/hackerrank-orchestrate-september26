import pytest

from data.db import Database


RAW_TABLES = [
    "financial_profiles",
    "financial_events",
    "exchange_rates",
    "requests",
    "request_payment_options",
    "images",
    "messages",
]


@pytest.fixture
def db():
    database = Database("buy_or_wait.db")
    database.initialize()

    yield database

    database.close()


@pytest.mark.parametrize("table", RAW_TABLES)
def test_table_contains_rows(db, table):
    row = db.execute(
        f"SELECT COUNT(*) AS count FROM {table}"
    ).fetchone()

    assert row["count"] > 0, f"{table} is empty"