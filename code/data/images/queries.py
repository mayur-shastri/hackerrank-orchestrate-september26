from data.db import Database
from .models import Image


def get_by_id(
    db: Database,
    image_id: str,
) -> Image | None:
    row = db.execute(
        """
        SELECT
            image_id,
            user_id,
            request_id,
            related_event_id
        FROM images
        WHERE image_id = ?
        """,
        (image_id,),
    ).fetchone()

    if row is None:
        return None

    return _to_model(row)


def get_for_event(
    db: Database,
    event_id: str,
) -> list[Image]:
    rows = db.execute(
        """
        SELECT
            image_id,
            user_id,
            request_id,
            related_event_id
        FROM images
        WHERE related_event_id = ?
        ORDER BY image_id ASC
        """,
        (event_id,),
    ).fetchall()

    return [_to_model(row) for row in rows]


def get_for_request(
    db: Database,
    request_id: str,
) -> list[Image]:
    rows = db.execute(
        """
        SELECT
            image_id,
            user_id,
            request_id,
            related_event_id
        FROM images
        WHERE request_id = ?
        ORDER BY image_id ASC
        """,
        (request_id,),
    ).fetchall()

    return [_to_model(row) for row in rows]


def _to_model(row) -> Image:
    return Image(
        image_id=row["image_id"],
        user_id=row["user_id"],
        request_id=row["request_id"],
        related_event_id=row["related_event_id"],
    )