import asyncio
import os
from crawl4ai import AsyncWebCrawler
from .crawl4ai_config.high_level.browser_config import get_browser_config
from .crawl4ai_config.high_level.crawl_config import get_crawl_config, get_html_file_crawl_config
from .crawl4ai_config.mid_level.dispatcher_config import get_semaphore_dispatcher, get_memory_adaptive_dispatcher
from .crawl4ai_config.mid_level.extraction_config import get_extraction_strategy
from .utils.url_utils import get_file_path_for_url
from .utils.file_utils import ensure_directory_exists, get_file_urls, print_file_list, save_markdowns, read_markdowns_from_folder


# Define base directories for storing files
FIT_HTML_DIR = os.path.join(os.path.dirname(__file__), "fit_html")
MARKDOWNS_DIR = os.path.join(os.path.dirname(__file__), "markdowns")


async def crawl(url: str, max_pages: int = None):
    # PHASE 1: Crawl pages quickly without LLM processing
    browser_conf = get_browser_config()
    crawler = await AsyncWebCrawler(config=browser_conf).start()
    crawl_config = get_crawl_config(max_pages=max_pages)

    # Execute the crawl and collect all results
    results = []
    saved_files = []  # Store the saved HTML filenames
    urls = []
    # Create fit_html directory if it doesn't exist
    ensure_directory_exists(FIT_HTML_DIR)

    async for result in await crawler.arun(url=url, config=crawl_config):
        results.append(result)
        urls.append(result.url)
        if result.success:
            # Get file path using utility function with the correct base directory
            file_path = get_file_path_for_url(result.url, base_dir=FIT_HTML_DIR)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result.markdown.fit_html)
            print(f"Saved HTML to {file_path}")
            saved_files.append(os.path.basename(file_path))  # Store just the filename
        else:
            print("Error:", result.error_message)

        score = result.metadata.get("score", 0)
        depth = result.metadata.get("depth", 0)
        print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

    print(f"Crawled {len(results)} pages")

    # await crawler.close()
    # https: // github.com / unclecode / crawl4ai / issues / 842
    return saved_files, urls
    # # PHASE 2: Process the saved HTML files
    # await create_markdowns(saved_files)


async def create_markdowns(saved_files: list[str], filter_prompt: str = None):
    """Process local HTML files using the crawler."""
    if not saved_files:
        print("No HTML files to process.")
        return

    # Convert filenames to file URLs with the correct base directory
    urls = get_file_urls(saved_files, base_dir=FIT_HTML_DIR)
    print_file_list(urls, "Processing HTML files:")

    # Create markdowns
    html_crawl_config = get_html_file_crawl_config(filter_prompt=filter_prompt)
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
                print(result.markdown.fit_markdown)
                successful_md_number+=1
            else:
                markdowns.append(None)
                print(f"Didn't process irrelevant page: {result.url}")
    print(f"Finished processing {successful_md_number} relevant links out of {len(urls)}")

    # Save markdowns to files with the correct base directory
    saved_markdown_files = save_markdowns(markdowns, base_dir=MARKDOWNS_DIR)
    print(f"Saved {len(saved_markdown_files)} markdown files")
    return markdowns
    # Process markdowns with LLM extraction
    # process_markdowns(markdowns)


def process_markdowns(markdowns=None, schema: dict = None, prompt: str = None):
    """
    Process markdowns with LLM extraction.
    
    Args:
        markdowns: List of markdown strings to process. If None, reads from markdowns folder.
        schema: Dictionary defining the schema for content extraction
        prompt: Text prompt for content extraction
    """
    # If markdowns is None, read from the markdowns folder
    # if markdowns is None:
    #     print("No markdowns provided, reading from markdowns folder...")
    #     markdowns = read_markdowns_from_folder(base_dir=MARKDOWNS_DIR)
    #     print(f"Read {len(markdowns)} markdowns from folder")
    
    contents = []

    # Process each page with LLM extraction
    i=1
    if markdowns:
        for md in markdowns:
            if md:
                print(f"Processing markdown {i}...")
                extraction_strategy = get_extraction_strategy(schema=schema, prompt=prompt)
                extracted_content = extraction_strategy.run(
                    url=str(i),
                    sections=[md]
                )
                contents.append(extracted_content)
                print(f"Extracted {len(extracted_content)} blocks from markdown {i}")
                i+=1
            else:
                print("None markdown")
                contents.append(None)
    print(contents)
    return contents


# if __name__ == "__main__":
#     # asyncio.run(main())
#     saved_files = ['www_ebay_com_dd4c0972_1743768602051.html', 'signup_ebay_com_740e3c5b_1743768604258.html', 'www_ebay_com_8924a7d5_1743768604638.html', 'signin_ebay_com_3aa3d089_1743768604796.html', 'www_ebay_com_e591f4a7_1743768606092.html', 'www_ebay_com_58b626cc_1743768606151.html', 'www_ebay_com_1cebd9a8_1743768606296.html', 'www_ebay_com_0e50deff_1743768606835.html', 'www_ebay_com_17c4c1d5_1743768606849.html', 'www_ebay_com_2885cb3d_1743768606866.html', 'www_ebay_com_d7cae06d_1743768606877.html', 'www_ebay_com_b59f75f8_1743768606919.html', 'www_ebay_com_21da5006_1743768606931.html', 'www_ebay_com_aebd674e_1743768607453.html', 'www_ebay_com_89cf3efd_1743768607612.html']
#     asyncio.run(create_markdowns(saved_files))
#     # process_markdowns()

