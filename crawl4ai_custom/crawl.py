import os
from crawl4ai import AsyncWebCrawler
from .crawl4ai_config.high_level.browser_config import get_browser_config
from .crawl4ai_config.high_level.crawl_config import get_crawl_config, get_html_file_crawl_config
from .crawl4ai_config.mid_level.dispatcher_config import get_semaphore_dispatcher, get_memory_adaptive_dispatcher
from .crawl4ai_config.mid_level.extraction_config import get_extraction_strategy
from .utils.url_utils import get_file_path_for_url
from .utils.file_utils import ensure_directory_exists, get_file_urls_from_list, print_file_list, save_markdowns, \
    read_markdowns_from_folder, generate_md_filename, save_markdown_content, read_markdown_file

# Define base directories for storing files
FIT_HTML_DIR = os.path.join(os.path.dirname(__file__), "fit_html")
MARKDOWNS_DIR = os.path.join(os.path.dirname(__file__), "markdowns")
NON_LLM_MARKDOWN_DIR = os.path.join(os.path.dirname(__file__), "non-llm-markdown")


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


def process_markdowns(markdowns=None, schema: dict = None, prompt: str = None):
    """
    Process markdowns with LLM extraction.
    
    Args:
        markdowns: List of markdown strings or filenames to process. If None, reads from markdowns folder.
        schema: Dictionary defining the schema for content extraction
        prompt: Text prompt for content extraction
    """
    contents = []

    # Process each page with LLM extraction
    i=1
    if markdowns:
        for md in markdowns:
            if md:
                print(f"Processing markdown {i}...")
                # Check if this is a file in the non-llm-markdown directory
                if isinstance(md, str) and os.path.exists(os.path.join(NON_LLM_MARKDOWN_DIR, md)):
                    md_content = read_markdown_file(md)
                    if not md_content:
                        contents.append(None)
                        continue
                else:
                    md_content = md

                extraction_strategy = get_extraction_strategy(schema=schema, prompt=prompt)
                extracted_content = extraction_strategy.run(
                    url=str(i),
                    sections=[md_content]
                )
                contents.append(extracted_content)
                print(f"Extracted {len(extracted_content)} blocks from markdown {i}")
                i+=1
            else:
                print("None markdown")
                contents.append(None)
    print(contents)
    return contents