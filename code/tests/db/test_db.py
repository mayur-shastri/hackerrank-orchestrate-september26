import sqlite3

from data.db import Database


EXPECTED_TABLES = {
    "financial_profiles",
    "financial_events",
    "exchange_rates",
    "requests",
    "request_payment_options",
    "images",
    "messages",
    "world_models",
}


def test_database_initializes(tmp_path):
    db_path = tmp_path / "test.db"

    db = Database(db_path)

    try:
        db.initialize()

        tables = {
            row["name"]
            for row in db.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }

        assert EXPECTED_TABLES.issubset(tables)

    finally:
        db.close()


def test_database_has_expected_columns(tmp_path):
    db_path = tmp_path / "test.db"

    db = Database(db_path)

    try:
        db.initialize()

        expected_columns = {
            "financial_profiles": {
                "user_id",
                "home_currency",
                "current_available_balance",
                "minimum_balance_to_keep",
                "financial_priorities",
                "expense_categories_to_protect",
                "expense_categories_user_is_willing_to_reduce",
                "expense_categories_user_is_willing_to_stop",
                "payment_methods_user_will_consider",
                "max_installment_months",
            },
            "financial_events": {
                "event_id",
                "user_id",
                "event_type",
                "description",
                "category",
                "direction",
                "amount",
                "currency",
                "event_date",
                "settlement_date",
                "status",
                "linked_event_id",
                "flexibility",
                "minimum_allowed_amount",
            },
            "exchange_rates": {
                "rate_date",
                "from_currency",
                "to_currency",
                "rate",
            },
            "requests": {
                "request_id",
                "user_id",
                "request_date",
                "request_type",
                "requested_amount",
                "desired_completion_date",
                "allows_partial_payment",
                "request_text",
            },
            "request_payment_options": {
                "payment_option_id",
                "request_id",
                "payment_method",
                "payment_amount",
                "number_of_payments",
                "first_payment_date",
                "payment_frequency_days",
                "financing_fee",
                "total_payable_amount",
            },
            "images": {
                "image_id",
                "user_id",
                "request_id",
                "related_event_id",
            },
            "messages": {
                "message_id",
                "user_id",
                "request_id",
                "related_event_id",
                "sent_at",
                "source_type",
                "message_text",
            },
            "world_models": {
                "user_id",
                "model_json",
                "updated_at",
            },
        }

        for table, expected in expected_columns.items():
            actual = {
                row["name"]
                for row in db.execute(
                    f"PRAGMA table_info({table})"
                ).fetchall()
            }

            assert expected == actual, (
                f"{table}: expected {expected}, got {actual}"
            )

    finally:
        db.close()


def test_database_creates_indexes(tmp_path):
    db_path = tmp_path / "test.db"

    db = Database(db_path)

    try:
        db.initialize()

        indexes = {
            row["name"]
            for row in db.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'index'
                """
            ).fetchall()
        }

        assert "idx_events_user_date" in indexes
        assert "idx_events_user_status_date" in indexes

    finally:
        db.close()