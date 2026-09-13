import os

from openai import  AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()

def get_openai_client() ->  AsyncOpenAI:
    return  AsyncOpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key="dummy",
    )

openai_client = get_openai_client()