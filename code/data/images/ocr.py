import base64
import mimetypes
import os
from pathlib import Path

from utils.llm import openai_client

BASE_DIR = Path(__file__).resolve().parents[2]
IMAGE_DIR = BASE_DIR / "dataset" / "media" / "images"

client = openai_client

def extract_image(image_id: str) -> str:
    image_path = IMAGE_DIR / f"{image_id}.png"

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image file not found for image_id={image_id}: {image_path}"
        )

    mime_type, _ = mimetypes.guess_type(image_path.name)

    if mime_type is None:
        raise ValueError(
            f"Could not determine image MIME type: {image_path}"
        )

    image_data = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    response = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract factual information from financial images. "
                    "Do not infer, calculate, or make financial judgments. "
                    "Extract only information visibly present in the image."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract all financially relevant information "
                            "visible in this image."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        },
                    },
                ],
            },
        ],
    )

    return response.choices[0].message.content or ""