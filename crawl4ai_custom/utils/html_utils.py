import re

def clean_nested_tags(html_content: str) -> str:
    """
    Clean up nested repeating tags in HTML content.
    For example: <span><span><span>text</span></span></span> becomes <span>text</span>
    
    Args:
        html_content: The HTML content to clean
        
    Returns:
        Cleaned HTML content
    """
    # Pattern to match nested repeating tags
    pattern = r'<([a-zA-Z]+)([^>]*)>(?:\s*<\1[^>]*>\s*)*([^<]+)(?:\s*</\1>\s*)*</\1>'
    
    def replace_nested(match):
        tag = match.group(1)
        attrs = match.group(2)
        content = match.group(3).strip()
        return f'<{tag}{attrs}>{content}</{tag}>'
    
    # Keep applying the pattern until no more nested tags are found
    while True:
        new_content = re.sub(pattern, replace_nested, html_content)
        if new_content == html_content:
            break
        html_content = new_content
    
    return html_content


def filter_long_links(html_content: str, max_link_length: int = 128) -> str:
    """
    Filter out links that are longer than max_link_length and clean up escaped slashes.
    
    Args:
        html_content: The HTML content to filter
        max_link_length: Maximum allowed length for href attributes
        
    Returns:
        Filtered HTML content
    """
    # First clean up nested tags
    html_content = clean_nested_tags(html_content)
    
    # Find all <a> tags with href attributes
    pattern = r'<a[^>]*href="([^"]*)"[^>]*>'
    
    def replace_long_link(match):
        href = match.group(1)
        # Clean up escaped slashes in the href
        clean_href = href.replace('\\\\\\', '').replace('\\\\', '').replace('\\"', '"')
        
        if len(clean_href) > max_link_length:
            # Replace the href with a placeholder
            return match.group(0).replace(href, "#")
        else:
            # Replace the href with cleaned version
            return match.group(0).replace(href, clean_href)
    
    # Replace long links and clean up slashes
    filtered_html = re.sub(pattern, replace_long_link, html_content)
    
    # Clean up any remaining escaped characters
    filtered_html = filtered_html.replace('\\\\\\', '').replace('\\\\', '').replace('\\"', '"')
    
    return filtered_html 