import base64
import mimetypes
import os
from pathlib import Path

from utils.llm import openai_client

IMAGE_MEDIA_DIR = Path(
    os.getenv("IMAGE_MEDIA_DIR", "dataset/media/images")
)

client = openai_client(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
)


def extract_image(image_id: str) -> str:
    image_path = IMAGE_MEDIA_DIR / image_id

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