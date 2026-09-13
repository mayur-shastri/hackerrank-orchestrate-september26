from data.db import Database
from .models import Message


def get_by_id(
    db: Database,
    message_id: str,
) -> Message | None:
    row = db.execute(
        """
        SELECT
            message_id,
            user_id,
            request_id,
            related_event_id,
            sent_at,
            source_type,
            message_text
        FROM messages
        WHERE message_id = ?
        """,
        (message_id,),
    ).fetchone()

    if row is None:
        return None

    return _to_model(row)


def get_for_event(
    db: Database,
    event_id: str,
) -> list[Message]:
    rows = db.execute(
        """
        SELECT
            message_id,
            user_id,
            request_id,
            related_event_id,
            sent_at,
            source_type,
            message_text
        FROM messages
        WHERE related_event_id = ?
        ORDER BY sent_at ASC, message_id ASC
        """,
        (event_id,),
    ).fetchall()

    return [_to_model(row) for row in rows]


def get_for_request(
    db: Database,
    request_id: str,
) -> list[Message]:
    rows = db.execute(
        """
        SELECT
            message_id,
            user_id,
            request_id,
            related_event_id,
            sent_at,
            source_type,
            message_text
        FROM messages
        WHERE request_id = ?
        ORDER BY sent_at ASC, message_id ASC
        """,
        (request_id,),
    ).fetchall()

    return [_to_model(row) for row in rows]


def _to_model(row) -> Message:
    return Message(
        message_id=row["message_id"],
        user_id=row["user_id"],
        request_id=row["request_id"],
        related_event_id=row["related_event_id"],
        sent_at=row["sent_at"],
        source_type=row["source_type"],
        message_text=row["message_text"],
    )