from datetime import datetime
from pathlib import Path

from data.db import Database
from data.financial_events.queries import (
    get_user_events_until,
    get_linked_event_trail,
)
from data.financial_profiles.queries import get_by_user_id
from data.exchange_rates.queries import get_rate
from data.messages.queries import get_for_event
from data.images.queries import get_for_event
from data.images.ocr import extract_image

import json
import os

from utils.llm import openai_client


client = openai_client

async def replay(
    db: Database,
    user_id: str,
    request_date: str,
) -> dict:
    """
    Replay all historical financial events for a user up to the
    request date and return the resulting world model.
    """

    profile = get_by_user_id(db, user_id)

    if profile is None:
        raise ValueError(
            f"No financial profile found for user_id={user_id}"
        )

    events = get_user_events_until(
        db,
        user_id,
        request_date,
    )

    world_model = {}

    for event in events:
        event_context = _build_event_context(
            db=db,
            event=event,
            profile=profile,
        )

        world_model = await update_world_model(
            world_model=world_model,
            event_context=event_context,
        )

    return world_model


def _build_event_context(
    db: Database,
    event,
    profile,
) -> dict:
    linked_events = get_linked_event_trail(
        db,
        event.event_id,
    )

    messages = []
    images = []

    for linked_event in linked_events:
        messages.extend(
            get_for_event(
                db,
                linked_event.event_id,
            )
        )

        images.extend(
            get_for_event(
                db,
                linked_event.event_id,
            )
        )

    linked_event_data = [
        _prepare_event(
            db=db,
            event=linked_event,
            home_currency=profile.home_currency,
        )
        for linked_event in linked_events
    ]

    image_extractions = []

    for image in images:
        extraction = extract_image(image.image_id)

        image_extractions.append(
            {
                "image_id": image.image_id,
                "related_event_id": image.related_event_id,
                "extracted_information": extraction,
            }
        )

    return {
        "event": _prepare_event(
            db=db,
            event=event,
            home_currency=profile.home_currency,
        ),
        "linked_events": linked_event_data,
        "messages": [
            {
                "message_id": message.message_id,
                "related_event_id": message.related_event_id,
                "sent_at": message.sent_at,
                "source_type": message.source_type,
                "message_text": message.message_text,
            }
            for message in messages
        ],
        "images": image_extractions,
    }


def _prepare_event(
    db: Database,
    event,
    home_currency: str,
) -> dict:
    data = {
        "event_id": event.event_id,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "description": event.description,
        "category": event.category,
        "direction": event.direction,
        "amount": event.amount,
        "currency": event.currency,
        "event_date": event.event_date,
        "settlement_date": event.settlement_date,
        "status": event.status,
        "linked_event_id": event.linked_event_id,
        "flexibility": event.flexibility,
        "minimum_allowed_amount": event.minimum_allowed_amount,
    }

    if (
        event.amount is not None
        and event.currency
        and event.currency != home_currency
    ):
        rate = get_rate(
            db=db,
            rate_date=event.event_date,
            from_currency=event.currency,
            to_currency=home_currency,
        )

        if rate is None:
            raise ValueError(
                f"No exchange rate found for "
                f"{event.currency}->{home_currency} "
                f"on {event.event_date}"
            )

        data["amount_in_home_currency"] = event.amount * rate
        data["home_currency"] = home_currency
        data["exchange_rate"] = rate

    else:
        data["amount_in_home_currency"] = event.amount
        data["home_currency"] = home_currency
        data["exchange_rate"] = 1.0

    return data


async def update_world_model(
    world_model: dict,
    event_context: dict,
) -> dict:
    """
    Update the world model by processing one financial event.

    The LLM receives the current world model and the complete
    context for the event, then returns the updated world model.
    """

    prompt = f"""
You are updating a user's financial world model based on a newly
processed financial event.

Your task is to update the existing world model using ONLY the
information provided in the current world model and event context.

CURRENT WORLD MODEL:
{json.dumps(world_model, indent=2)}

EVENT CONTEXT:
{json.dumps(event_context, indent=2)}

Instructions:
- Preserve information from the existing world model unless the new
  event provides evidence that it should be updated.
- Incorporate information from the current event and its linked
  events.
- Use associated messages and extracted image information as evidence.
- Do not invent facts.
- Do not make affordability or purchase recommendations.
- Keep the world model factual and useful for future forecasting.
- Return ONLY the complete updated world model as valid JSON.
"""

    response = await client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You maintain a structured financial world model. "
                    "Return only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("World model LLM returned an empty response")

    try:
        updated_world_model = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "World model LLM returned invalid JSON"
        ) from exc

    if not isinstance(updated_world_model, dict):
        raise ValueError(
            "World model LLM response must be a JSON object"
        )

    return updated_world_model