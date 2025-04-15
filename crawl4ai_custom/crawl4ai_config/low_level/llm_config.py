import os
from dotenv import load_dotenv
from crawl4ai import LLMConfig
import litellm

# Enable LiteLLM debug mode
litellm._turn_on_debug()

load_dotenv()
api_token = os.getenv("API_TOKEN")

def get_llm_config():
    return LLMConfig(
        provider="openai/gpt-4",
        api_token=api_token,
        temprature=0.1,
        max_tokens=1000
    )
