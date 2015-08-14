''' signals and handlers
'''

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def user_saved(sender=None, instance=None, **kwargs):
    print "User models post_save signal hander", instance, kwargs


@receiver(post_delete, sender=User)
def user_deleted(sender=None, instance=None, **kwargs):
    print "User models post_delete signal hander", instance, kwargs
