import os
from dotenv import load_dotenv
from crawl4ai import LLMConfig

load_dotenv()
api_token = os.getenv("API_TOKEN")

def get_llm_config():
    return LLMConfig(
        provider="openai/gpt-4o-mini",
        api_token=api_token
    )
