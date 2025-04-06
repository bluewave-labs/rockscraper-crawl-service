import hashlib
import time
import os


def get_domain_from_url(url: str) -> str:
    """Extract domain from URL and replace dots with underscores."""
    return url.split('://')[1].split('/')[0].replace('.', '_')


def generate_html_filename(url: str, timestamp: int = None) -> str:
    """Generate a unique filename for HTML content based on URL and timestamp."""
    if timestamp is None:
        timestamp = int(time.time() * 1000)  # Millisecond timestamp
    
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    domain = get_domain_from_url(url)
    return f"{domain}_{url_hash}_{timestamp}.html"


def get_file_path_for_url(url: str, base_dir: str = "fit_html") -> str:
    """Generate full file path for HTML content based on URL."""
    filename = generate_html_filename(url)
    return os.path.join(base_dir, filename) 