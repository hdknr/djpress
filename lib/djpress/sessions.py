# coding: utf-8
from django.conf import settings
import hashlib


def set_wp_user(request, id):
    key = getattr(settings, 'DJPRESS_KEY', settings.SECRET_KEY)
    if key:
        session_key = request.session.session_key
        digest = hashlib.sha256("{0}{1}{2}".format(
            session_key, id, key)).hexdigest()
    else:
        digest = ''
    request.session['wp_user'] = "{0}:{1}".format(id, digest)
