import csv
import json
from pathlib import Path
from typing import Any


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return rows as dictionaries."""
    path = Path(path)

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def clean(value: str | None) -> str | None:
    """Strip whitespace and convert empty values to None."""
    if value is None:
        return None

    value = value.strip()
    return value if value else None


def to_float(value: str | None) -> float | None:
    """Convert a CSV value to float."""
    value = clean(value)
    return float(value) if value is not None else None


def to_int(value: str | None) -> int | None:
    """Convert a CSV value to int."""
    value = clean(value)
    return int(value) if value is not None else None


def to_bool(value: str | None) -> int | None:
    """
    Convert common boolean representations to SQLite-compatible integers.
    Returns None for empty values.
    """
    value = clean(value)

    if value is None:
        return None

    normalized = value.lower()

    if normalized in {"true", "1", "yes"}:
        return 1

    if normalized in {"false", "0", "no"}:
        return 0

    raise ValueError(f"Invalid boolean value: {value}")


def to_json(value: str | None) -> str | None:
    """
    Normalize a structured CSV field into a JSON string.

    If the value is already valid JSON, preserve its structure.
    Otherwise store the value as a JSON string.
    """
    value = clean(value)

    if value is None:
        return None

    try:
        parsed: Any = json.loads(value)
        return json.dumps(parsed)
    except (json.JSONDecodeError, TypeError):
        return json.dumps(value)