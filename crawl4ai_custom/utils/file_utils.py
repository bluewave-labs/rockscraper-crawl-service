import os
from typing import List


def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists, create it if it doesn't."""
    os.makedirs(directory, exist_ok=True)


def get_file_urls(filenames: List[str], base_dir: str = "fit_html") -> List[str]:
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
            
        filename = f"markdown_{i}.md"
        file_path = os.path.join(base_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        saved_files.append(filename)
        print(f"Saved markdown to {file_path}")
    
    return saved_files


def read_markdowns_from_folder(base_dir: str = "markdowns") -> List[str]:
    """
    Read all markdown files from the specified directory.
    
    Args:
        base_dir: Directory to read markdowns from
        
    Returns:
        List of markdown strings
    """
    # Ensure the directory exists
    ensure_directory_exists(base_dir)
    
    markdowns = []
    markdown_files = [f for f in os.listdir(base_dir) if f.endswith('.md')]
    
    for filename in sorted(markdown_files):
        file_path = os.path.join(base_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            markdown = f.read()
            markdowns.append(markdown)
            print(f"Read markdown from {file_path}")
    
    return markdowns 