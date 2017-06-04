# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create,
#   * modify, and delete the table
# Feel free to rename the models,
#   * but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of
# 'django-admin sqlcustom [app_label]' into your database.

from __future__ import unicode_literals

from . import wordpress, methods, querysets


class WpCommentmeta(wordpress.WpCommentmeta):

    class Meta:
        managed = False
        db_table = 'wp_commentmeta'


class WpComments(wordpress.WpComments):

    class Meta:
        managed = False
        db_table = 'wp_comments'


class WpLinks(wordpress.WpLinks):

    class Meta:
        managed = False
        db_table = 'wp_links'


class WpOptions(wordpress.WpOptions):

    class Meta:
        managed = False
        db_table = 'wp_options'


class WpPostmeta(wordpress.WpPostmeta):

    class Meta:
        managed = False
        db_table = 'wp_postmeta'


class WpPosts(wordpress.WpPosts):

    class Meta:
        managed = False
        db_table = 'wp_posts'


class WpTermRelationships(wordpress.WpTermRelationships):

    class Meta:
        managed = False
        db_table = 'wp_term_relationships'
        unique_together = (('object_id', 'term_taxonomy_id'),)


class WpTermTaxonomy(wordpress.WpTermTaxonomy):

    class Meta:
        managed = False
        db_table = 'wp_term_taxonomy'
        unique_together = (('term_id', 'taxonomy'),)


class WpTerms(wordpress.WpTerms):

    class Meta:
        managed = False
        db_table = 'wp_terms'


class WpUsermeta(wordpress.WpUsermeta):

    class Meta:
        managed = False
        db_table = 'wp_usermeta'

    def __unicode__(self):
        return u"{} - {}:{}".format(
            self.user and self.user.__unicode__(),
            self.meta_key, self.meta_value)


class WpUsers(wordpress.WpUsers, methods.WpUsers):

    class Meta:
        managed = False
        db_table = 'wp_users'

    objects = querysets.WpUsersrQuerySet.as_manager()

    def __unicode__(self):
        return self.user_login
