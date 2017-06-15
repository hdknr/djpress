# coding: utf-8
import django
import logging
logger = logging.getLogger()

Base = object

if django.VERSION >= (1, 11):
    from django.utils.deprecation import MiddlewareMixin as Base


class Middleware(Base):

    def process_response(self, request, response):
        ''' if user has been logged out, no session data , so no 'wp_user'
        '''
        wp_user = request.session.get('wp_user', None)

        if wp_user and request.user.is_authenticated():
            response.set_cookie('WP_USER', wp_user or '')
            try:
                response.set_cookie('USER_ID', request.user.id)
            except:
                pass
        else:
            for i in ['WP_USER', 'USER_ID']:
                try:
                    response.delete_cookie(i)
                except:
                    pass

        return response
