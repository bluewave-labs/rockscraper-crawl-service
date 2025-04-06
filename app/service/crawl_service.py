import asyncio
from datetime import datetime
from app import db
from app.helper.db.db_utils import save_to_db
from app.models.crawl_model import Crawls
from crawl4ai_custom.crawl import crawl, create_markdowns, process_markdowns

class CrawlService:
    async def _perform_crawl(self, url):
        """
        Perform the actual crawling using crawl4ai_custom
        
        Args:
            url (str): URL to crawl
            
        Returns:
            tuple: (markdown, html, extracted_content)
        """
        # Run the crawl
        saved_files = await crawl()
        
        # Process the HTML files into markdowns
        markdowns = await create_markdowns(saved_files)
        
        # Process markdowns to extract content
        extracted_contents = process_markdowns(markdowns)
        
        # For now, return the first result
        return (
            extracted_contents[0] if extracted_contents else None,  # markdown
            None,  # html (would come from crawl results)
            extracted_contents[0] if extracted_contents else None  # extracted_content
        )

    def crawl_website(self, url, user_id):
        """
        Crawl a website and store the results
        
        Args:
            url (str): URL to crawl
            user_id (int): ID of the user requesting the crawl
            
        Returns:
            Crawls: The created crawl record
        """
        try:
            # Run the async crawl
            markdown, html, extracted_content = asyncio.run(self._perform_crawl(url))
            
            # Create the crawl record
            crawl_record = Crawls(
                user_id=user_id,
                url=url,
                markdown=markdown,
                html=html,
                extracted_content=extracted_content,
                date=datetime.now(timezone.utc)
            )
            
            # Save to database
            success, result, error_message = save_to_db(crawl_record)

            if not success:
                raise Exception(error_message)

            return result
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to crawl website: {str(e)}") 