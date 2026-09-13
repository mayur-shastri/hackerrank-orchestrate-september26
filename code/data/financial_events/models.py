from dataclasses import dataclass
from typing import Any


@dataclass
class FinancialEvent:
    event_id: str
    user_id: str
    event_type: str | None
    description: str | None
    category: str | None
    direction: str | None
    amount: float | None
    currency: str | None
    event_date: str | None
    settlement_date: str | None
    status: str | None
    linked_event_id: str | None
    flexibility: str | None
    minimum_allowed_amount: float | None


@dataclass
class EventContext:
    event: FinancialEvent
    linked_events: list[FinancialEvent]
    messages: list[dict[str, Any]]
    images: list[dict[str, Any]]
    financial_profile: Any