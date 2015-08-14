from django.conf import settings
import logging
log = logging.getLogger()

URLS = [
    'STATIC_URL',
    'LOGIN_URL',
    'LOGOUT_URL',
    'LOGIN_REDIRECT_URL', ]


class SettingsMiddleware(object):
    def process_request(self, request):
        prefix = request.META.get('SCRIPT_NAME')

        if prefix:
            for i in URLS:
                val = getattr(settings, i, None)
                if val and not val.startswith(prefix):
                    setattr(settings, i, prefix + val)
