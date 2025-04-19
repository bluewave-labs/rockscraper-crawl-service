from crawl4ai import AsyncWebCrawler
from .crawl4ai_config.high_level.browser_config import get_browser_config
from .crawl4ai_config.high_level.crawl_config import get_html_file_crawl_config
from .crawl4ai_config.mid_level.dispatcher_config import get_memory_adaptive_dispatcher
from .utils.file_utils import get_file_urls_from_list, print_file_list, save_markdowns, NON_LLM_MARKDOWN_DIR, MARKDOWNS_DIR
import os

async def create_markdowns(saved_files: list[str], filter_prompt: str = None, ignore_images: bool = True, ignore_links: bool = True):
    """Process local markdown files using the crawler."""
    if not saved_files:
        print("No markdown files to process.")
        return

    # Convert filenames to file URLs with the correct base directory
    urls = get_file_urls_from_list(saved_files, base_dir=NON_LLM_MARKDOWN_DIR)
    print_file_list(urls, "Processing markdown files:")

    # Create markdowns
    html_crawl_config = get_html_file_crawl_config(filter_prompt=filter_prompt, ignore_images=ignore_images, ignore_links=ignore_links)
    markdowns = []
    successful_md_number = 0
    dispatcher = get_memory_adaptive_dispatcher()
    browser_conf = get_browser_config()
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        async for result in await crawler.arun_many(urls=urls, config=html_crawl_config):
            if result.success:
                markdowns.append(result.markdown.fit_markdown)
                print(f"Successfully processed: {result.url}")
                print("Markdown Content:")
                successful_md_number += 1
            else:
                markdowns.append(None)
                print(f"Didn't process irrelevant page: {result.url}")
    print(f"Finished processing {successful_md_number} relevant links out of {len(urls)}")

    # Save markdowns to files with the correct base directory
    saved_markdown_files = save_markdowns(markdowns, base_dir=MARKDOWNS_DIR)
    print(f"Saved {len(saved_markdown_files)} markdown files")
    return markdowns 