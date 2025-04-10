from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai_custom.crawl4ai_config.low_level.llm_config import get_llm_config

def get_extraction_strategy(schema: dict = None, prompt: str = None):

    return LLMExtractionStrategy(
        llm_config=get_llm_config(),
        schema=schema,
        extraction_type="schema",
        instruction=prompt,
        chunk_token_threshold=800,
        overlap_rate=0.2,
        apply_chunking=True,
        input_format="markdown",
        extra_args={
            "temperature": 0.1,
            "max_tokens": 1000,
            # "truncate": True
        },
        verbose=True,
        # max_workers=4
    ) 