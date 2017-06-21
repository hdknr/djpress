# coding: utf-8

from __future__ import unicode_literals
from django.utils.functional import cached_property
import phpserialize
from . import sessions, xmlrpc, signals
from logging import getLogger
import traceback

logger = getLogger()


class WpUsers(object):

    def set_meta(self, meta_key, meta_value):
        if self.wpusermeta_set.filter(meta_key=meta_key).update(meta_value=meta_value) < 1:      # NOQA
            self.wpusermeta_set.create(
                meta_key=meta_key, meta_value=meta_value)

    def get_meta(self, meta_key):
        return self.wpusermeta_set.filter(meta_key=meta_key).first()

    def delete_meta(self, meta_key):
        self.wpusermeta_set.filter(meta_key=meta_key).delete()

    def set_metas_for(
            self, djuser, display_name=None,
            description=None, user_level=None, **kwargs):

        if not user_level:
            user_level = 10 if djuser.is_superuser else 1

        display_name = display_name or u"{} {}".format(
            djuser.last_name or '', djuser.first_name or '')
        if display_name == u' ':
            display_name = djuser.username

        self.set_meta('wp_user_level',  user_level)
        self.set_meta('first_name',  djuser.first_name)
        self.set_meta('last_name',  djuser.last_name)
        self.set_meta('show_admin_bar_front', False)

        self.set_nickname(display_name)
        self.set_description(description)

        cap = {'subscriber': True}
        if user_level == 10:
            cap = {'contributer': True, 'administrator': True, }
        self.set_meta('wp_capabilities', phpserialize.dumps(cap))

        for key, value in kwargs.items():
            self.set_meta(key, value)

    @classmethod
    def set_session(cls, request, wpuser_id):
        sessions.set_wp_user(request, wpuser_id)

    def set_nickname(self, nickname):
        self.set_meta('nickname', nickname)

    def set_description(self, description):
        self.set_meta('description', description)

    def set_avatar(self, image_url, image):
        if not image_url:
            self.delete_meta('wp_user_avatar')
            return

        try:
            post = xmlrpc.upload_image(image_url, image)
            self.set_meta('wp_user_avatar', post['id'])
        except:
            logger.error(traceback.format_exc())

    def get_avatar(self):
        return self.get_meta('wp_user_avatar')


class WpPosts(object):

    def add_thumbnail(self,  id):
        meta_key = '_thumbnail_id'
        return self.set_meta(meta_key, id)

    def set_thumbnail(self, image_url, image):
        try:
            post = xmlrpc.upload_image(image_url, image)
            self.set_meta('_thumbnail_id', post['id'])
            signals.thumbnail_uploaded.send(
                sender=type(self), instance=self, response=post)
        except:
            logger.error(traceback.format_exc())

    def set_meta(self, meta_key, meta_value):
        meta = self.get_meta(meta_key)
        if meta:
            meta.meta_value = meta_value
            meta.save()
            return meta
        else:
            return self.wppostmeta_set.create(
                meta_key=meta_key, meta_value=meta_value)

    def get_meta(self, meta_key):
        return self.wppostmeta_set.filter(meta_key=meta_key).first()


class WpPostmeta(object):

    @cached_property
    def value_dict(self):
        return self.meta_value and phpserialize.loads(self.meta_value) or {}
