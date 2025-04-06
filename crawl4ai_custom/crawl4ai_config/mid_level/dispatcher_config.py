from crawl4ai import DisplayMode
from crawl4ai.async_dispatcher import SemaphoreDispatcher, RateLimiter, CrawlerMonitor, MemoryAdaptiveDispatcher

def get_semaphore_dispatcher():
    return SemaphoreDispatcher(
        max_session_permit=20,         # Maximum concurrent tasks
        rate_limiter=RateLimiter(      # Optional rate limiting
            base_delay=(0.5, 1.0),
            max_delay=10.0
        ),
        # monitor=CrawlerMonitor(        # Optional monitoring
        #     max_visible_rows=15,
        #     display_mode=DisplayMode.DETAILED
        # )
    )


def get_memory_adaptive_dispatcher():
    return MemoryAdaptiveDispatcher(
        memory_threshold_percent=90.0,  # Pause if memory exceeds this
        check_interval=1.0,             # How often to check memory
        max_session_permit=10,          # Maximum concurrent tasks
        rate_limiter=RateLimiter(       # Optional rate limiting
            base_delay=(1.0, 2.0),
            max_delay=30.0,
            max_retries=2
        ),
        # monitor=CrawlerMonitor(         # Optional monitoring
        #     max_visible_rows=15,
        #     display_mode=DisplayMode.DETAILED
        # )
    )