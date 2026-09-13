import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

def get_openai_client() -> OpenAI:
    return OpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key="dummy",
    )

openai_client = get_openai_client()