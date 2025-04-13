from crawl4ai import DefaultMarkdownGenerator, PruningContentFilter, LLMContentFilter
from crawl4ai_custom.crawl4ai_config.low_level.llm_config import get_llm_config

def get_llm_filter(filter_prompt:str = None):
    return LLMContentFilter(
        llm_config=get_llm_config(),
        instruction=filter_prompt,
        chunk_token_threshold=500,  # Adjust based on your needs
        verbose=True,
        extra_args={
            "temperature": 0.1,
            "max_tokens": 1000,
            # "truncate": True
        },
        # max_workers=15
    )

def get_pruning_filter():
    return PruningContentFilter(
        threshold=0.40,
        threshold_type="fixed",  # or "dynamic"
        min_word_threshold=1
    )

def get_pruning_md_generator(ignore_images=True, ignore_links=True):
    return DefaultMarkdownGenerator(
        content_filter=get_pruning_filter(),
        options={
            "ignore_images": ignore_images,
            "ignore_links": ignore_links,
            "body_width": 80
        }
    )

def get_llm_md_generator(filter_prompt:str = None, ignore_images=True, ignore_links=True):
    return DefaultMarkdownGenerator(
        content_filter=get_llm_filter(filter_prompt=filter_prompt),
        options={
            "ignore_images": ignore_images,
            "ignore_links": ignore_links,
            "body_width": 80
        }
    )
