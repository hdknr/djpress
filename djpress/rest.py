from django.core.cache import cache 
import requests
from . import conf


def api_posts():
    return f'{conf.API}/posts?_embed'


def api_post(id):
    return f'{conf.API}/posts/{id}?_embed'


def wordpress_json(url): 
    return cache.get(url) or cache.get_or_set(
        url, requests.get(url).json())

    
def get_posts():
    return wordpress_json(api_posts())


def get_post(id):
    return wordpress_json(api_post(id))