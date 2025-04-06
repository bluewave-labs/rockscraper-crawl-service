from crawl4ai import BrowserConfig

def get_browser_config():
    return BrowserConfig(
        headless=True,
        viewport_width=1280,
        viewport_height=720
    ) 