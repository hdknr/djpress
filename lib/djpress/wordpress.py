# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `abstract = True` lines if you wish to allow Django to create,
#   * modify, and delete the table
# Feel free to rename the models,
#   * but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of
# 'django-admin sqlcustom [app_label]' into your database.

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PositiveBigAutoField(models.BigAutoField):
    empty_strings_allowed = False
    description = _("Big (8 byte) positive integer")

    def db_type(self, connection):
        """
        Returns MySQL-specific column data type. Make additional checks
        to support other backends.
        """
        return 'bigint UNSIGNED'

    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': models.BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super(PositiveBigAutoField, self).formfield(**defaults)


class WpCommentmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    comment_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class WpComments(models.Model):
    comment_id = models.BigIntegerField(db_column='comment_ID', primary_key=True)  # Field name made lowercase.  # NOQA
    comment_post_id = models.BigIntegerField(db_column='comment_post_ID')  # Field name made lowercase.  # NOQA
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=100)
    comment_author_url = models.CharField(max_length=200)
    comment_author_ip = models.CharField(db_column='comment_author_IP', max_length=100)  # Field name made lowercase.   # NOQA
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField()
    comment_content = models.TextField()
    comment_karma = models.IntegerField()
    comment_approved = models.CharField(max_length=20)
    comment_agent = models.CharField(max_length=255)
    comment_type = models.CharField(max_length=20)
    comment_parent = models.BigIntegerField()
    user_id = models.BigIntegerField()

    class Meta:
        abstract = True


class WpLinks(models.Model):
    link_id = models.BigIntegerField(primary_key=True)
    link_url = models.CharField(max_length=255)
    link_name = models.CharField(max_length=255)
    link_image = models.CharField(max_length=255)
    link_target = models.CharField(max_length=25)
    link_description = models.CharField(max_length=255)
    link_visible = models.CharField(max_length=20)
    link_owner = models.BigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=255)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=255)

    class Meta:
        abstract = True


class WpOptions(models.Model):
    option_id = models.BigIntegerField(primary_key=True)
    option_name = models.CharField(unique=True, max_length=64)
    option_value = models.TextField()
    autoload = models.CharField(max_length=20)

    class Meta:
        abstract = True


class WpPosts(models.Model):
    # id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.     # NOQA
    # id = models.BigAutoField(primary_key=True, db_column='ID')
    id = PositiveBigAutoField(primary_key=True, db_column='ID')
    post_author = models.BigIntegerField()
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=20)
    comment_status = models.CharField(max_length=20)
    ping_status = models.CharField(max_length=20)
    post_password = models.CharField(max_length=20)
    post_name = models.CharField(max_length=200)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=255)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=20)
    post_mime_type = models.CharField(max_length=100)
    comment_count = models.BigIntegerField()

    class Meta:
        abstract = True


class WpPostmeta(models.Model):
    # meta_id = models.BigIntegerField(primary_key=True)
    meta_id = models.BigAutoField(primary_key=True)
    # post_id = models.BigIntegerField()
    post = models.ForeignKey('WpPosts', db_column='post_id')
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class WpTermRelationships(models.Model):
    object_id = models.BigIntegerField()
    term_taxonomy_id = models.BigIntegerField()
    term_order = models.IntegerField()

    class Meta:
        abstract = True


class WpTermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key=True)
    term_id = models.BigIntegerField()
    taxonomy = models.CharField(max_length=32)
    description = models.TextField()
    parent = models.BigIntegerField()
    count = models.BigIntegerField()

    class Meta:
        abstract = True


class WpTerms(models.Model):
    term_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    term_group = models.BigIntegerField()

    class Meta:
        abstract = True


class WpUsermeta(models.Model):
    # umeta_id = models.BigIntegerField(primary_key=True)
    umeta_id = models.BigAutoField(primary_key=True)
    # user_id = models.BigIntegerField()
    user = models.ForeignKey('WpUsers', db_column='user_id')
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class WpUsers(models.Model):
    # id = models.BigIntegerField(db_column='ID', primary_key=True)
    id = models.BigAutoField(db_column='ID', primary_key=True)
    user_login = models.CharField(max_length=60)
    user_pass = models.CharField(max_length=64)
    user_nicename = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=60)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=250)

    class Meta:
        abstract = True
