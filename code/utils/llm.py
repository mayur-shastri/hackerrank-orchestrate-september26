import os

from openai import  AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()

def get_openai_client() ->  AsyncOpenAI:
    return  AsyncOpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
         max_retries=0,
    )

openai_client = get_openai_client()