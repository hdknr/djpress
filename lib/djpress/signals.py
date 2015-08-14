''' signals and handlers
'''

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from wordpress import WpUsers
import uuid


@receiver(post_save, sender=User)
def user_saved(sender=None, instance=None, **kwargs):
    if instance:
        user = WpUsers.objects.filter(
            user_login=instance.username).first()
        if not user:
            WpUsers.objects.create(
                user_login=instance.username,
                user_nicename=instance.username,
                user_status=not instance.is_active and 1 or 0,
                user_pass=uuid.uuid1().hex,
                user_registered=instance.date_joined,
                user_email=instance.email,
                display_name=instance.username,
                )
        else:
            user.user_status = not instance.is_active and 1 or 0
            user.user_email = instance.email
            user.display_name = instance.username
            user.save()


@receiver(post_delete, sender=User)
def user_deleted(sender=None, instance=None, **kwargs):
    if instance:
        WpUsers.objects.filter(user_login=instance.username).delete()
