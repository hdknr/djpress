# coding: utf-8

from __future__ import unicode_literals
import phpserialize
from . import sessions


class WpUsers(object):

    def set_meta(self, meta_key, meta_value):
        if self.wpusermeta_set.filter(meta_key=meta_key).update(meta_value=meta_value) < 1:      # NOQA
            self.wpusermeta_set.create(
                meta_key=meta_key, meta_value=meta_value)

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

    def set_avatar(self, post_id):
        self.set_meta('wp_user_avatar', post_id)


class WpPosts(object):

    def add_thumbnail(self,  id):
        meta_key = '_thumbnail_id'
        thumbnail, created = self.wppostmeta_set.get_or_create(
            meta_key=meta_key, meta_value=id)
        return thumbnail
