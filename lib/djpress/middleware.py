import logging
logger = logging.getLogger()


class Middleware(object):
    def process_response(self, request, response):
        ''' if user has been logged out, no session data , so no 'wp_user'
        '''
        wp_user = request.session.get('wp_user', None)
        response.set_cookie('WP_USER', wp_user or '')
        try:
            response.set_cookie('USER_ID', request.user.id)
        except:
            pass
        return response
