from data.db import Database
from .models import ExchangeRate


def get_rate(
    db: Database,
    rate_date: str,
    from_currency: str,
    to_currency: str,
) -> ExchangeRate | None:
    row = db.execute(
        """
        SELECT
            rate_date,
            from_currency,
            to_currency,
            rate
        FROM exchange_rates
        WHERE rate_date = ?
          AND from_currency = ?
          AND to_currency = ?
        """,
        (rate_date, from_currency, to_currency),
    ).fetchone()

    if row is None:
        return None

    return ExchangeRate(
        rate_date=row["rate_date"],
        from_currency=row["from_currency"],
        to_currency=row["to_currency"],
        rate=row["rate"],
    )