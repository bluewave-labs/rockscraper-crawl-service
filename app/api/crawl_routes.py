from app.api import bp
from app.controller import crawl_controller
from app.middleware.auth_middleware import verify_jwt

@bp.route('/crawl', methods=['POST'])
# @verify_jwt
def crawl_website(user_id=123):
    return crawl_controller.crawl_website_controller(user_id)

@bp.route('/crawls', methods=['GET'])
# @verify_jwt
def get_all_crawls():
    return crawl_controller.get_all_crawls_controller()