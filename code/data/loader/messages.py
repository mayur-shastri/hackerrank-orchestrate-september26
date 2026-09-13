from pathlib import Path

from data.db import Database
from .common import read_csv, clean


def load_messages(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "messages.csv")

    query = """
        INSERT OR REPLACE INTO messages (
            message_id,
            user_id,
            request_id,
            related_event_id,
            sent_at,
            source_type,
            message_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    values = [
        (
            clean(row["message_id"]),
            clean(row["user_id"]),
            clean(row["request_id"]),
            clean(row["related_event_id"]),
            clean(row["sent_at"]),
            clean(row["source_type"]),
            clean(row["message_text"]),
        )
        for row in rows
    ]

    result = db.executemany(query, values)
    print(result.rowcount, "messages loaded")