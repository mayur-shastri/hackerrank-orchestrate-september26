from dataclasses import dataclass


@dataclass
class ExchangeRate:
    rate_date: str
    from_currency: str
    to_currency: str
    rate: float