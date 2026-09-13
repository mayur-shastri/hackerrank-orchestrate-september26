from data.db import Database
from .models import FinancialProfile

import json


def get_by_user_id(
    db: Database,
    user_id: str,
) -> FinancialProfile | None:
    row = db.execute(
        """
        SELECT
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
        FROM financial_profiles
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    if row is None:
        return None

    return FinancialProfile(
        user_id=row["user_id"],
        home_currency=row["home_currency"],
        current_available_balance=row["current_available_balance"],
        minimum_balance_to_keep=row["minimum_balance_to_keep"],
        financial_priorities=_parse_json(row["financial_priorities"]),
        expense_categories_to_protect=_parse_json(
            row["expense_categories_to_protect"]
        ),
        expense_categories_user_is_willing_to_reduce=_parse_json(
            row["expense_categories_user_is_willing_to_reduce"]
        ),
        expense_categories_user_is_willing_to_stop=_parse_json(
            row["expense_categories_user_is_willing_to_stop"]
        ),
        payment_methods_user_will_consider=_parse_json(
            row["payment_methods_user_will_consider"]
        ),
        max_installment_months=row["max_installment_months"],
    )


def _parse_json(value: str | None) -> list[str]:
    if not value:
        return []

    return json.loads(value)