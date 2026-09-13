from pathlib import Path

from data.db import Database
from .common import read_csv, clean


def load_images(
    db: Database,
    dataset_dir: str | Path,
) -> None:
    rows = read_csv(Path(dataset_dir) / "images.csv")

    query = """
        INSERT OR REPLACE INTO images (
            image_id,
            user_id,
            request_id,
            related_event_id
        )
        VALUES (?, ?, ?, ?)
    """

    values = [
        (
            clean(row["image_id"]),
            clean(row["user_id"]),
            clean(row["request_id"]),
            clean(row["related_event_id"]),
        )
        for row in rows
    ]

    result = db.executemany(query, values)
    print(result)