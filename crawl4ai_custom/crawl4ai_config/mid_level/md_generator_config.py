from crawl4ai import DefaultMarkdownGenerator, PruningContentFilter, LLMContentFilter
from crawl4ai_custom.crawl4ai_config.low_level.llm_config import get_llm_config

def get_llm_filter():
    return LLMContentFilter(
        llm_config=get_llm_config(),
        instruction="""
    Create a brief markdown file. Only include important details.
    Include:
    - Important headers
    - Posted date
    - Source
    Exclude:
    - Navigation elements
    - Sidebars
    - Footer content
    - Menu elements like login/signup
    - Comments
    - Points
    """,
        chunk_token_threshold=500,  # Adjust based on your needs
        verbose=True,
        # max_workers=15
    )

def get_pruning_filter():
    return PruningContentFilter(
        threshold=0.40,
        threshold_type="fixed",  # or "dynamic"
        min_word_threshold=1
    )

def get_pruning_md_generator():
    return DefaultMarkdownGenerator(
        content_filter=get_pruning_filter(),
        options={
            "ignore_images": True,
            "ignore_links": True,
            "body_width": 80
        }
    )

def get_llm_md_generator():
    return DefaultMarkdownGenerator(
        content_filter=get_llm_filter(),
        options={
            "ignore_images": True,
            "ignore_links": True,
            "body_width": 80
        }
    )
