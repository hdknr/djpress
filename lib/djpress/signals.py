''' signals and handlers
'''

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

import uuid
import hashlib

from wordpress import WpUsers
import phpserialize


@receiver(post_save, sender=User)
def user_saved(sender=None, instance=None, **kwargs):
    if instance:
        user_level = 10 if instance.is_superuser else 1
        wpuser = WpUsers.objects.filter(
            user_login=instance.username).first()

        display_name = u"{} {}".format(
            instance.last_name or '',
            instance.first_name or '',)
        if display_name == u' ':
            display_name = instance.username

        def setmeta():
            wpuser = WpUsers.objects.filter(
                user_login=instance.username).first()
            if not wpuser:
                return

            wpuser.set_meta('wp_user_level',  user_level)
            wpuser.set_meta('first_name',  instance.first_name)
            wpuser.set_meta('last_name',  instance.last_name)
            wpuser.set_meta('nickname',  display_name)

            if user_level == 10:
                cap = {
                    'contributer': True,
                    'administrator': True, }
                wpuser.set_meta(
                    'wp_capabilities',
                    phpserialize.dumps(cap))

        with transaction.atomic():
            transaction.on_commit(setmeta)
            if not wpuser:
                wpuser = WpUsers.objects.create(
                    user_login=instance.username,
                    user_nicename=instance.username,
                    user_status=not instance.is_active and 1 or 0,
                    user_pass=uuid.uuid1().hex,
                    user_registered=instance.date_joined,
                    user_email=instance.email,
                    display_name=display_name,
                    )
            else:
                wpuser.user_status = not instance.is_active and 1 or 0
                wpuser.user_email = instance.email
                wpuser.display_name = display_name
                wpuser.save()


@receiver(post_delete, sender=User)
def user_deleted(sender=None, instance=None, **kwargs):
    if instance:
        WpUsers.objects.filter(user_login=instance.username).delete()


def set_wp_user(request, id):
    key = getattr(settings, 'DJPRESS_KEY', None)
    if key:
        session_key = request.session.session_key
        digest = hashlib.sha256("{0}{1}{2}".format(
            session_key, id, key)).hexdigest()
    else:
        digest = ''
    request.session['wp_user'] = "{0}:{1}".format(id, digest)


@receiver(user_logged_in)
def user_loggedin(sender=None, request=None, user=None, **kwargs):
    wp_user = user and WpUsers.objects.filter(user_login=user.username).first()
    if wp_user:
        set_wp_user(request, wp_user.id)
