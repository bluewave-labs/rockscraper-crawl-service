from app.api import bp
from app.controller import crawl_controller

bp.route('/crawl', methods=['POST'])(crawl_controller.crawl_website_controller)