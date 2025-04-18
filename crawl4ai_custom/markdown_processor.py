import multiprocessing
multiprocessing.set_start_method('spawn', True)

from multiprocessing import Process, Queue, cpu_count
from .crawl4ai_config.mid_level.extraction_config import get_extraction_strategy

def process_single_markdown(markdown_tuple, result_queue, schema: dict = None, prompt: str = None):
    """
    Process a single markdown with LLM extraction.
    
    Args:
        markdown_tuple: Tuple of (name, content) to process
        result_queue: Queue to store the results
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
    result_queue.put((name, extracted_content))

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
    
    # Create a queue for results
    result_queue = Queue()
    processes = []
    results = {}

    # Start processes
    for i in range(0, len(markdowns), num_processes):
        batch = markdowns[i:i + num_processes]
        for markdown_tuple in batch:
            p = Process(target=process_single_markdown, args=(markdown_tuple, result_queue, schema, prompt))
            processes.append(p)
            p.start()

        # Wait for batch to complete
        for p in processes:
            p.join()

        # Collect results
        while not result_queue.empty():
            name, content = result_queue.get()
            results[name] = content

    # Convert results to list in original order
    contents = [results.get(name, None) for name, _ in markdowns]
    print(contents)
    return contents 