import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query: str, params=()):
        return self.conn.execute(query, params)

    def executemany(self, query: str, params):
        return self.conn.executemany(query, params)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def initialize(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS financial_profiles (
            user_id TEXT PRIMARY KEY,
            home_currency TEXT,
            current_available_balance REAL NOT NULL,
            minimum_balance_to_keep REAL NOT NULL,
            financial_priorities TEXT,
            expense_categories_to_protect TEXT,
            expense_categories_user_is_willing_to_reduce TEXT,
            expense_categories_user_is_willing_to_stop TEXT,
            payment_methods_user_will_consider TEXT,
            max_installment_months INTEGER
        );

        CREATE TABLE IF NOT EXISTS financial_events (
            event_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            event_type TEXT,
            description TEXT,
            category TEXT,
            direction TEXT,
            amount REAL,
            currency TEXT,
            event_date TEXT,
            settlement_date TEXT,
            status TEXT,
            linked_event_id TEXT,
            flexibility TEXT,
            minimum_allowed_amount REAL
        );

        CREATE INDEX IF NOT EXISTS idx_events_user_date
        ON financial_events(user_id, event_date);

        CREATE INDEX IF NOT EXISTS idx_events_user_status_date
        ON financial_events(user_id, status, event_date);

        CREATE TABLE IF NOT EXISTS exchange_rates (
            rate_date TEXT NOT NULL,
            from_currency TEXT NOT NULL,
            to_currency TEXT NOT NULL,
            rate REAL NOT NULL,
            PRIMARY KEY (rate_date, from_currency, to_currency)
        );

        CREATE TABLE IF NOT EXISTS requests (
            request_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            request_date TEXT,
            request_type TEXT,
            requested_amount REAL,
            desired_completion_date TEXT,
            allows_partial_payment INTEGER,
            request_text TEXT
        );

        CREATE TABLE IF NOT EXISTS request_payment_options (
            payment_option_id TEXT PRIMARY KEY,
            request_id TEXT NOT NULL,
            payment_method TEXT,
            payment_amount REAL,
            number_of_payments INTEGER,
            first_payment_date TEXT,
            payment_frequency_days INTEGER,
            financing_fee REAL,
            total_payable_amount REAL
        );

        CREATE TABLE IF NOT EXISTS images (
            image_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            request_id TEXT,
            related_event_id TEXT
        );

        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            request_id TEXT,
            related_event_id TEXT,
            sent_at TEXT,
            source_type TEXT,
            message_text TEXT
        );

        CREATE TABLE IF NOT EXISTS world_models (
            user_id TEXT PRIMARY KEY,
            model_json TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)

        self.conn.commit()