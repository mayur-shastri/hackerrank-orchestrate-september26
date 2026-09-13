from dataclasses import dataclass


@dataclass
class Message:
    message_id: str
    user_id: str
    request_id: str | None
    related_event_id: str | None
    sent_at: str | None
    source_type: str | None
    message_text: str | None