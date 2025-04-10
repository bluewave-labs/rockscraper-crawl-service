from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy
from crawl4ai.browser_manager import BrowserManager


async def patched_async_playwright__crawler_strategy_close(self) -> None:
    """
    Close the browser and clean up resources.

    This patch addresses an issue with Playwright instance cleanup where the static instance
    wasn't being properly reset, leading to issues with multiple crawls.

    Issue: https://github.com/unclecode/crawl4ai/issues/842

    Returns:
        None
    """
    await self.browser_manager.close()

    # Reset the static Playwright instance
    BrowserManager._playwright_instance = None


AsyncPlaywrightCrawlerStrategy.close = patched_async_playwright__crawler_strategy_close