# coding: utf-8
from django.conf import settings
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.compat import xmlrpc_client
import os
import mimetypes

XMLRPC = getattr(
    settings, 'DJPRESS_XMLRPC', {'URL': '', 'USER': '', 'PASSWORD': ''})


def client(url=None, user=None, password=None):
    url = url or XMLRPC['URL']
    user = user or XMLRPC['USER']
    password = password or XMLRPC['PASSWORD']
    return Client(url, user, password)


def upload_image(image_url, image,  wp=None):

    wp = wp or client()

    data = {
        'name': os.path.basename(image_url),
        'type': mimetypes.guess_type(image_url)[0],
        'overwrite': True,
        'bits': xmlrpc_client.Binary(image),
    }
    return wp.call(media.UploadFile(data))
