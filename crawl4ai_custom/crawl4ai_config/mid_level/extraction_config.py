from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai_custom.crawl4ai_config.low_level.llm_config import get_llm_config

def get_extraction_strategy():
    schema = {
        'product_name': 'product_name',
        'price': 'price'
    }

    return LLMExtractionStrategy(
        llm_config=get_llm_config(),
        schema=schema,
        extraction_type="schema",
        instruction="This is a ecommerce website. Extract a list of items from the webpage with 'product name' and 'price' fields. If it isn't a product or doesn't have a price don't include it",
        chunk_token_threshold=1200,
        overlap_rate=0.1,
        apply_chunking=True,
        input_format="markdown",
        extra_args={"temperature": 0.1, "max_tokens": 1000},
        verbose=True,
        # max_workers=4
    ) 