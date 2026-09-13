from data.db import Database
from .models import FinancialEvent


def get_by_id(
    db: Database,
    event_id: str,
) -> FinancialEvent | None:
    row = db.execute(
        """
        SELECT
            event_id,
            user_id,
            event_type,
            description,
            category,
            direction,
            amount,
            currency,
            event_date,
            settlement_date,
            status,
            linked_event_id,
            flexibility,
            minimum_allowed_amount
        FROM financial_events
        WHERE event_id = ?
        """,
        (event_id,),
    ).fetchone()

    if row is None:
        return None

    return _to_model(row)


def get_user_events_until(
    db: Database,
    user_id: str,
    request_date: str,
) -> list[FinancialEvent]:
    rows = db.execute(
        """
        SELECT
            event_id,
            user_id,
            event_type,
            description,
            category,
            direction,
            amount,
            currency,
            event_date,
            settlement_date,
            status,
            linked_event_id,
            flexibility,
            minimum_allowed_amount
        FROM financial_events
        WHERE user_id = ?
          AND event_date <= ?
        ORDER BY event_date ASC, event_id ASC
        """,
        (user_id, request_date),
    ).fetchall()

    return [_to_model(row) for row in rows]


def get_scheduled_events(
    db: Database,
    user_id: str,
    start_date: str,
    end_date: str,
) -> list[FinancialEvent]:
    rows = db.execute(
        """
        SELECT
            event_id,
            user_id,
            event_type,
            description,
            category,
            direction,
            amount,
            currency,
            event_date,
            settlement_date,
            status,
            linked_event_id,
            flexibility,
            minimum_allowed_amount
        FROM financial_events
        WHERE user_id = ?
          AND event_date > ?
          AND event_date <= ?
        ORDER BY event_date ASC, event_id ASC
        """,
        (user_id, start_date, end_date),
    ).fetchall()

    return [_to_model(row) for row in rows]


def get_linked_event_trail(
    db: Database,
    event_id: str,
) -> list[FinancialEvent]:
    """
    Follow linked_event_id recursively until the beginning
    of the linked-event chain.

    Example:
        E3 -> E2 -> E1

    Starting from E3 returns:
        E3, E2, E1
    """

    rows = db.execute(
        """
        WITH RECURSIVE event_chain AS (
            SELECT
                event_id,
                user_id,
                event_type,
                description,
                category,
                direction,
                amount,
                currency,
                event_date,
                settlement_date,
                status,
                linked_event_id,
                flexibility,
                minimum_allowed_amount,
                0 AS depth
            FROM financial_events
            WHERE event_id = ?

            UNION ALL

            SELECT
                e.event_id,
                e.user_id,
                e.event_type,
                e.description,
                e.category,
                e.direction,
                e.amount,
                e.currency,
                e.event_date,
                e.settlement_date,
                e.status,
                e.linked_event_id,
                e.flexibility,
                e.minimum_allowed_amount,
                ec.depth + 1
            FROM financial_events e
            JOIN event_chain ec
                ON e.event_id = ec.linked_event_id
        )
        SELECT
            event_id,
            user_id,
            event_type,
            description,
            category,
            direction,
            amount,
            currency,
            event_date,
            settlement_date,
            status,
            linked_event_id,
            flexibility,
            minimum_allowed_amount
        FROM event_chain
        ORDER BY depth ASC
        """,
        (event_id,),
    ).fetchall()

    return [_to_model(row) for row in rows]

def _to_model(row) -> FinancialEvent:
    return FinancialEvent(
        event_id=row["event_id"],
        user_id=row["user_id"],
        event_type=row["event_type"],
        description=row["description"],
        category=row["category"],
        direction=row["direction"],
        amount=row["amount"],
        currency=row["currency"],
        event_date=row["event_date"],
        settlement_date=row["settlement_date"],
        status=row["status"],
        linked_event_id=row["linked_event_id"],
        flexibility=row["flexibility"],
        minimum_allowed_amount=row["minimum_allowed_amount"],
    )