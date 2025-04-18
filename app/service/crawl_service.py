import asyncio
import json
from datetime import datetime, timezone
from app import db
from app.helper.db.db_utils import save_to_db
from app.models.crawl_model import Crawls
from crawl4ai_custom.crawler import crawl
from crawl4ai_custom.markdown_creator import create_markdowns
from crawl4ai_custom.markdown_processor import process_markdowns
from crawl4ai_custom.utils.file_utils import NON_LLM_MARKDOWN_DIR
import os

class CrawlService:
    async def _perform_crawl(self, url: str, max_pages=None, max_depth=1, extraction_schema=None, extraction_prompt=None, markdown_filter_prompt=None, ignore_images=True, ignore_links=True, is_llm_markdown=False):
        """
        Perform the actual crawling using crawl4ai_custom
        
        Args:
            url (str): URL to crawl
            max_pages (int, optional): Maximum number of pages to crawl
            max_depth (int, optional): Maximum depth to crawl. Defaults to 1.
            extraction_schema (dict, optional): Schema for content extraction
            extraction_prompt (str, optional): Prompt for content extraction
            markdown_filter_prompt (str, optional): Prompt for filtering markdown content
            ignore_images (bool, optional): Whether to ignore images in markdown. Defaults to True.
            ignore_links (bool, optional): Whether to ignore links in markdown. Defaults to True.
            is_llm_markdown (bool, optional): Whether to skip LLM markdown processing. Defaults to False.
            
        Returns:
            tuple: (markdown_content, html, extracted_content, urls)
        """
        # Run the crawl
        saved_files, urls = await crawl(url, max_pages=max_pages, max_depth=max_depth, ignore_images=ignore_images, ignore_links=ignore_links)
        
        # Get the actual markdown content
        markdown_content = []
        for filename in saved_files:
            with open(os.path.join(NON_LLM_MARKDOWN_DIR, filename), 'r', encoding='utf-8') as f:
                markdown_content.append(f.read())
        
        # Process the markdown content if needed
        if is_llm_markdown:
            markdown_content = await create_markdowns(saved_files, filter_prompt=markdown_filter_prompt, ignore_images=ignore_images, ignore_links=ignore_links)
        
        # Process markdowns to extract content
        extracted_contents = None
        if extraction_schema or extraction_prompt:
            # Create tuples of (filename_without_extension, content) for concurrent processing
            markdown_tuples = [(os.path.splitext(filename)[0], content) for filename, content in zip(saved_files, markdown_content) if content is not None]
            extracted_contents = process_markdowns(
                markdowns=markdown_tuples,
                schema=extraction_schema,
                prompt=extraction_prompt
            )
        
        return (
            markdown_content,
            saved_files,
            extracted_contents,
            urls
        )

    def crawl_website(self, url, user_id, max_pages=None, max_depth=1, extraction_schema=None, extraction_prompt=None, markdown_filter_prompt=None, ignore_images=True, ignore_links=True, is_llm_markdown=False):
        """
        Crawl a website and store the results
        
        Args:
            url (str): URL to crawl
            user_id (int): ID of the user requesting the crawl
            max_pages (int, optional): Maximum number of pages to crawl
            max_depth (int, optional): Maximum depth to crawl. Defaults to 1.
            extraction_schema (dict, optional): Schema for content extraction
            extraction_prompt (str, optional): Prompt for content extraction
            markdown_filter_prompt (str, optional): Prompt for filtering markdown content
            ignore_images (bool, optional): Whether to ignore images in markdown. Defaults to True.
            ignore_links (bool, optional): Whether to ignore links in markdown. Defaults to True.
            is_llm_markdown (bool, optional): Whether to skip LLM markdown processing. Defaults to False.
            
        Returns:
            Crawls: The created crawl record
        """
        try:
            # Run the async crawl
            markdown_content, html, extracted_content, urls = asyncio.run(self._perform_crawl(
                url,
                max_pages=max_pages,
                max_depth=max_depth,
                extraction_schema=extraction_schema,
                extraction_prompt=extraction_prompt,
                markdown_filter_prompt=markdown_filter_prompt,
                ignore_images=ignore_images,
                ignore_links=ignore_links,
                is_llm_markdown=is_llm_markdown
            ))

            assert(len(markdown_content) == len(html))
            if extracted_content:
                assert (len(markdown_content) == len(extracted_content))
      
            
            # Create and save crawl records one by one
            saved_records = []
            for i in range(len(markdown_content)):
                # Convert individual items to JSON strings for database storage
                markdown_item = markdown_content[i] if markdown_content and markdown_content[i] is not None else None
                html_item = html[i] if html else None
                extracted_content_item = json.dumps(extracted_content[i]) if extracted_content and extracted_content[i] is not None else None
                crawl_url = urls[i] if urls else None
                
                # Create the crawl record
                crawl_record = Crawls(
                    user_id=user_id,
                    url=crawl_url,
                    markdown=markdown_item,
                    html=html_item,
                    extracted_content=extracted_content_item,
                    date=datetime.now(timezone.utc)
                )
                
                # Save to database
                success, result, error_message = save_to_db(crawl_record)
                
                if not success:
                    db.session.rollback()
                    raise Exception(f"Failed to save crawl record {i}: {error_message}")
                
                saved_records.append(result)
            
            return saved_records
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to crawl website: {str(e)}")

    def get_all_crawls(self, page=1, per_page=10):
        """
        Get all crawls with pagination
        
        Args:
            page (int): Page number (1-based)
            per_page (int): Number of items per page
            
        Returns:
            Pagination: Paginated query result containing crawls
        """
        try:
            # Query all crawls ordered by date descending
            query = Crawls.query.order_by(Crawls.date.desc())
            
            # Return paginated results
            return query.paginate(page=page, per_page=per_page, error_out=False)
            
        except Exception as e:
            raise Exception(f"Failed to fetch crawls: {str(e)}") 