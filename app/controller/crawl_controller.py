from flask import jsonify, request
from app.service.crawl_service import CrawlService
from app.models.crawl_model import Crawls
from errors import bad_request

def validate_crawl_data(data):
    """
    Validate the input data for crawling a website.
    :param data: The input dictionary to validate.
    :return: Boolean indicating if validation passed, or raises BadRequest if validation fails.
    """
    # Type checks
    if not isinstance(data.get('url'), str):
        return bad_request("URL must be a string")

    if not isinstance(data.get('user_id'), int):
        return bad_request("User ID must be an integer")

    if 'max_pages' in data and not isinstance(data.get('max_pages'), int):
        return bad_request("max_pages must be an integer")

    if 'max_depth' in data and not isinstance(data.get('max_depth'), int):
        return bad_request("max_depth must be an integer")

    if 'ignore_images' in data and not isinstance(data.get('ignore_images'), bool):
        return bad_request("ignore_images must be a boolean")

    if 'ignore_links' in data and not isinstance(data.get('ignore_links'), bool):
        return bad_request("ignore_links must be a boolean")

    if 'is_llm_markdown' in data and not isinstance(data.get('is_llm_markdown'), bool):
        return bad_request("is_llm_markdown must be a boolean")

    if 'extraction_schema' in data and not isinstance(data.get('extraction_schema'), dict):
        return bad_request("extraction_schema must be a dictionary")

    if 'extraction_prompt' in data and not isinstance(data.get('extraction_prompt'), str):
        return bad_request("extraction_prompt must be a string")

    if 'markdown_filter_prompt' in data and not isinstance(data.get('markdown_filter_prompt'), str):
        return bad_request("markdown_filter_prompt must be a string")

    # Null checks
    required_fields = ['url', 'user_id']
    for field in required_fields:
        if not data.get(field):
            return bad_request(f"{field.capitalize()} is required")

    return True

def crawl_website_controller():
    """
    Controller to process website URL and crawl its content.
    """
    # Step 1: Validate input
    data = request.get_json()
    validation_response = validate_crawl_data(data)
    if validation_response is not True:
        return validation_response

    url = data['url']
    user_id = data['user_id']
    max_pages = data.get('max_pages')
    max_depth = data.get('max_depth', 1)  # Default to 1 if not provided
    ignore_images = data.get('ignore_images', True)  # Default to True if not provided
    ignore_links = data.get('ignore_links', True)  # Default to True if not provided
    is_llm_markdown = data.get('is_llm_markdown', False)  # Default to False if not provided
    extraction_schema = data.get('extraction_schema')
    extraction_prompt = data.get('extraction_prompt')
    markdown_filter_prompt = data.get('markdown_filter_prompt')

    try:
        # Step 2: Call service to perform crawl
        crawl_service = CrawlService()
        results = crawl_service.crawl_website(
            url=url,
            user_id=user_id,
            max_pages=max_pages,
            max_depth=max_depth,
            extraction_schema=extraction_schema,
            extraction_prompt=extraction_prompt,
            markdown_filter_prompt=markdown_filter_prompt,
            ignore_images=ignore_images,
            ignore_links=ignore_links,
            is_llm_markdown=is_llm_markdown
        )

        # Step 3: Return the response
        return jsonify({
            'success': True,
            'data': [result.to_dict() for result in results] if results else None
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_all_crawls_controller():
    """
    Controller to fetch all crawls with pagination.
    """
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1:
            return bad_request("Page number must be greater than 0")
        if per_page < 1:
            return bad_request("Items per page must be greater than 0")
            
        # Call service to get paginated crawls
        crawl_service = CrawlService()
        paginated_crawls = crawl_service.get_all_crawls(page=page, per_page=per_page)
        
        # Return the response
        return jsonify({
            'success': True,
            'data': {
                'items': [crawl.to_dict() for crawl in paginated_crawls.items],
                'total': paginated_crawls.total,
                'pages': paginated_crawls.pages,
                'current_page': paginated_crawls.page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 