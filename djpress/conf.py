from django.conf import settings


DJPRESS = getattr(settings, 'DJPRESS', {})
REMOTE = DJPRESS.get('REMOTE', 'http://localhost')
PATH = DJPRESS.get('PATH', '/wp-json/wp/v2')
API = f'{REMOTE}{PATH}'

