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

    try:
        # Step 2: Call service to perform crawl
        crawl_service = CrawlService()
        result = crawl_service.crawl_website(url=url, user_id=user_id)

        # Step 3: Return the response
        return jsonify({
            'success': True,
            'data': result.to_dict() if result else None
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 