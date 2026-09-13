from dataclasses import dataclass


@dataclass
class Image:
    image_id: str
    user_id: str
    request_id: str | None
    related_event_id: str | None