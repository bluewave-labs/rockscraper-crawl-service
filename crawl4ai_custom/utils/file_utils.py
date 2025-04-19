import os
from typing import List
import time
import re
from urllib.parse import urlparse

# Define base directories for storing files
NON_LLM_MARKDOWN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "non-llm-markdown")
MARKDOWNS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "markdowns")
FIT_HTML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fit_html")

def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists, create it if it doesn't."""
    os.makedirs(directory, exist_ok=True)


def get_file_url(filename: str, base_dir: str = "fit_html") -> str:
    """Convert filenames to file URLs."""
    return f"file://{os.path.abspath(os.path.join(base_dir, filename))}"

def get_file_urls_from_list(filenames: List[str], base_dir: str = "fit_html") -> List[str]:
    """Convert filenames to file URLs."""
    return [f"file://{os.path.abspath(os.path.join(base_dir, filename))}" for filename in filenames]


def print_file_list(files: List[str], message: str = "Files to process:") -> None:
    """Print a list of files with a custom message."""
    print(f"{message} {len(files)}")
    for file in files:
        print(f"  - {file}")


def save_markdowns(markdowns: List[str], base_dir: str = "markdowns") -> List[str]:
    """
    Save markdowns to files in the specified directory.
    
    Args:
        markdowns: List of markdown strings to save
        base_dir: Directory to save markdowns in
        
    Returns:
        List of filenames where markdowns were saved
    """
    # Ensure the directory exists
    ensure_directory_exists(base_dir)
    
    saved_files = []
    for i, markdown in enumerate(markdowns, 1):
        # Skip None values
        if markdown is None:
            print(f"Skipping None markdown at index {i}")
            continue
            
        # Generate filename using the new function
        filename = generate_md_filename(f"markdown_{i}", is_markdown=True)
        file_path = os.path.join(base_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        saved_files.append(filename)
        print(f"Saved markdown to {file_path}")
    
    return saved_files


def read_markdowns_from_folder(base_dir: str = "markdowns") -> List[tuple]:
    """
    Read all markdown files from the specified directory.
    
    Args:
        base_dir: Directory to read markdowns from
        
    Returns:
        List of tuples containing (filename, markdown_content)
    """
    # Ensure the directory exists
    ensure_directory_exists(base_dir)
    
    markdowns = []
    markdown_files = [f for f in os.listdir(base_dir) if f.endswith('.md')]
    
    for filename in sorted(markdown_files):
        file_path = os.path.join(base_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            markdown = f.read()
            # Store as tuple (filename without .md extension, content)
            markdowns.append((os.path.splitext(filename)[0], markdown))
            print(f"Read markdown from {file_path}")
    
    return markdowns


def generate_md_filename(url: str, timestamp: int = None, is_markdown=True) -> str:
    """Generate a unique filename for MD content based on URL and timestamp."""
    if timestamp is None:
        timestamp = int(time.time() * 1000)  # Millisecond timestamp
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Get the domain and path
    domain = parsed.netloc.replace('.', '_')
    path = parsed.path.strip('/').replace('/', '_')
    
    # If path is empty, use a default name
    if not path:
        path = 'index'
    
    # Remove any invalid characters
    filename = f"{domain}_{path}"
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    
    # Ensure the filename isn't too long
    if len(filename) > 255:
        filename = filename[:255]
    
    # Add timestamp and appropriate extension
    extension = ".md" if is_markdown else ".html"
    return f"{filename}_{timestamp}{extension}"

def save_markdown_content(content: str, url: str, base_dir: str, is_markdown: bool = True) -> str:
    """
    Save markdown or HTML content to a file with proper path generation.
    
    Args:
        content: The content to save
        url: The URL associated with the content
        base_dir: Base directory to save the file in
        is_markdown: Whether the content is markdown (True) or HTML (False)
        
    Returns:
        The filename where the content was saved
    """
    # Ensure the directory exists
    ensure_directory_exists(base_dir)
    
    # Generate filename and create full path
    filename = generate_md_filename(url, is_markdown=is_markdown)
    file_path = os.path.join(base_dir, filename)
    
    # Save the content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved {'markdown' if is_markdown else 'HTML'} to {file_path}")
    return filename

def read_markdown_file(filename: str, base_dir: str = None) -> str:
    """
    Read markdown content from a file.
    
    Args:
        filename: The filename to read from
        base_dir: The base directory where the file is located. If None, uses the default non-llm-markdown directory.
        
    Returns:
        str: The markdown content or None if there was an error
    """
    if base_dir is None:
        # Get the absolute path to the non-llm-markdown directory
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "non-llm-markdown")


    try:
        file_path = os.path.join(base_dir, filename)
        print(f"Reading markdown file from: {file_path}")  # Debug print
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading markdown file {filename} from {base_dir}: {str(e)}")
        return None