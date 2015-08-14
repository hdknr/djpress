import logging
logger = logging.getLogger()


class Middleware(object):
    def process_response(self, request, response):
        wp_user = request.session.get('wp_user', None)
        if wp_user:
            response.set_cookie('WP_USER', wp_user)
        return response
