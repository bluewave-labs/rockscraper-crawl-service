from multiprocessing import Pool, cpu_count, get_context
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
    Process markdowns with LLM extraction concurrently.
    
    Args:
        markdowns: List of markdown tuples (name, content) to process. If None, reads from markdowns folder.
        schema: Dictionary defining the schema for content extraction
        prompt: Text prompt for content extraction
    """
    if not markdowns:
        return []

    # Use 3 processes or the number of available CPU cores, whichever is smaller
    num_processes = min(3, cpu_count())
    print(f"Using {num_processes} processes for concurrent extraction")

    # Create a process pool with spawn context and map the processing function
    with get_context("spawn").Pool(processes=num_processes) as pool:
        contents = pool.map(lambda x: process_single_markdown(x, schema, prompt), markdowns)

    print(contents)
    return contents 