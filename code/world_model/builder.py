import json
import os
from typing import Any

from openai import OpenAI


SYSTEM_PROMPT = """
You maintain a user's financial world model.

Given:
1. The current world model
2. A newly processed financial event
3. The complete linked-event trail associated with that event
4. Messages associated with those events

Update the world model to reflect what is known after processing this event.

Rules:
- Preserve information from the existing world model unless the new information changes it.
- Incorporate useful facts, financial patterns, obligations, income, expenses, and other relevant state.
- Do not invent information that is not supported by the provided context.
- Monetary amounts are already converted to the user's home currency.
- Return ONLY the updated world model as valid JSON.
"""


class WorldModelBuilder:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.client = OpenAI(
            base_url=base_url or os.environ["LLM_BASE_URL"],
            api_key=api_key or os.environ["LLM_API_KEY"],
        )

        self.model = model or os.environ["LLM_MODEL"]

    def update(
        self,
        current_world_model: dict[str, Any],
        event: dict[str, Any],
        linked_events: list[dict[str, Any]],
        messages: list[dict[str, Any]],
    ) -> dict[str, Any]:
        payload = {
            "current_world_model": current_world_model,
            "event": event,
            "linked_events": linked_events,
            "messages": messages,
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        payload,
                        ensure_ascii=False,
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("LLM returned an empty world model")

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON for the world model"
            ) from exc