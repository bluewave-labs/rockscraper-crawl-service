from crawl4ai import CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from math import inf as infinity

from crawl4ai_custom.crawl4ai_config.mid_level.extraction_config import get_extraction_strategy
from crawl4ai_custom.crawl4ai_config.mid_level.md_generator_config import get_pruning_md_generator, get_llm_md_generator

def get_crawl_config(max_pages:int = infinity, max_depth:int = 1):
    return CrawlerRunConfig(
        verbose=True,
        stream=True,
        cache_mode=CacheMode.DISABLED,
        markdown_generator=get_pruning_md_generator(),
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth,
            max_pages=max_pages,
        )
    )

def get_html_file_crawl_config(filter_prompt:str = None):
    return CrawlerRunConfig(
        cache_mode=CacheMode.DISABLED,
        verbose=True,
        stream=True,
        markdown_generator=get_llm_md_generator(filter_prompt),
        # extraction_strategy=get_extraction_strategy()
    )