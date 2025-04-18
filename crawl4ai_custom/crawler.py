import os
from crawl4ai import AsyncWebCrawler
from .crawl4ai_config.high_level.browser_config import get_browser_config
from .crawl4ai_config.high_level.crawl_config import get_crawl_config
from .utils.file_utils import ensure_directory_exists, save_markdown_content, NON_LLM_MARKDOWN_DIR

async def crawl(url: str, max_pages: int = None, max_depth: int = 1, ignore_images: bool = True, ignore_links: bool = True):
    # PHASE 1: Crawl pages quickly without LLM processing
    browser_conf = get_browser_config()
    crawler = await AsyncWebCrawler(config=browser_conf).start()
    crawl_config = get_crawl_config(max_pages=max_pages, max_depth=max_depth, ignore_images=ignore_images, ignore_links=ignore_links)

    # Execute the crawl and collect all results
    results = []

    saved_files = []  # Store the saved HTML filenames
    urls = []
    # Create non-llm-markdown directory if it doesn't exist
    ensure_directory_exists(NON_LLM_MARKDOWN_DIR)

    async for result in await crawler.arun(url=url, config=crawl_config):
        results.append(result)
        urls.append(result.url)
        if result.success:
            # Save markdown content using the utility function
            filename = save_markdown_content(
                content=result.markdown.fit_markdown,
                url=result.url,
                base_dir=NON_LLM_MARKDOWN_DIR,
                is_markdown=True
            )
            saved_files.append(filename)
        else:
            print("Error:", result.error_message)

        score = result.metadata.get("score", 0)
        depth = result.metadata.get("depth", 0)
        print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

    print(f"Crawled {len(results)} pages")

    # await crawler.close()
    # https: // github.com / unclecode / crawl4ai / issues / 842
    return saved_files, urls 