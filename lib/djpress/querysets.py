# coding: utf-8
from django.db import models
from django.db import transaction


import uuid


def wp_nicename(djuser):
    return u"{}-{}".format(
        djuser.id,
        djuser.email.replace('@', '').replace('.',  '-'), )


class WpUsersrQuerySet(models.QuerySet):

    @transaction.atomic
    def create_user(self, djuser, **params):
        wpuser = None

        display_name = u"{} {}".format(
            djuser.last_name or '',
            djuser.first_name or '',)
        if display_name == u' ':
            display_name = djuser.username

        wpuser = self.create(
            user_login=djuser.username,
            user_nicename=wp_nicename(djuser),
            user_status=not djuser.is_active and 1 or 0,
            user_pass=uuid.uuid1().hex,
            user_registered=djuser.date_joined,
            user_email=djuser.email,
            display_name=display_name,
        )
        wpuser.set_metas_for(
            djuser, display_name=display_name, **params)

        return wpuser

    def find_by_meta(self, meta_key, meta_value):
        return self.filter(
            wpusermeta__meta_key=meta_key,
            wpusermeta__meta_value=meta_value)
