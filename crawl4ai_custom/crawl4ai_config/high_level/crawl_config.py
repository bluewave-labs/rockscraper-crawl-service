from crawl4ai import CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

from crawl4ai_custom.crawl4ai_config.mid_level.extraction_config import get_extraction_strategy
from crawl4ai_custom.crawl4ai_config.mid_level.md_generator_config import get_pruning_md_generator, get_llm_md_generator

def get_crawl_config():
    return CrawlerRunConfig(
        verbose=True,
        stream=True,
        cache_mode=CacheMode.DISABLED,
        markdown_generator=get_pruning_md_generator(),
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=1,
            max_pages=5,
        )
    )

def get_html_file_crawl_config():
    return CrawlerRunConfig(
        cache_mode=CacheMode.DISABLED,
        verbose=True,
        stream=True,
        markdown_generator=get_llm_md_generator(),
        # extraction_strategy=get_extraction_strategy()
    )