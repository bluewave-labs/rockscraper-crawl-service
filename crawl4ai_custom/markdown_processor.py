from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from .crawl4ai_config.mid_level.extraction_config import get_extraction_strategy

def process_single_markdown(markdown_tuple, schema: dict = None, prompt: str = None):
    """
    Process a single markdown with LLM extraction.
    
    Args:
        markdown_tuple: Tuple of (name, content) to process
        schema: Dictionary defining the schema for content extraction
        prompt: Text prompt for content extraction
    """
    name, md = markdown_tuple
    print(f"Processing markdown {name}...")
    extraction_strategy = get_extraction_strategy(schema=schema, prompt=prompt)
    extracted_content = extraction_strategy.run(
        url=name,
        sections=[md]
    )
    print(f"Extracted {len(extracted_content)} blocks from markdown {name}")
    return extracted_content

def process_markdowns(markdowns=None, schema: dict = None, prompt: str = None):
    """
    Process markdowns with LLM extraction concurrently using threads.
    
    Args:
        markdowns: List of markdown tuples (name, content) to process. If None, reads from markdowns folder.
        schema: Dictionary defining the schema for content extraction
        prompt: Text prompt for content extraction
    """
    if not markdowns:
        return []

    # Use 3 threads or the number of available CPU cores, whichever is smaller
    num_threads = min(3, cpu_count())
    print(f"Using {num_threads} threads for concurrent extraction")

    with Pool(processes=num_threads) as pool:
        contents = pool.map(process_single_markdown, markdowns[:3])

    print(contents)
    return contents