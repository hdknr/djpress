from django.contrib import admin
from django.apps import apps


def register(module_name, admins, ignore_models=[]):
    ''' Regiter Admin UI  '''
    app_label = module_name.split('.')[-2:][0]
    for model in apps.get_app_config(app_label).get_models():

        if model.__name__ in ignore_models:
            continue
        name = "%sAdmin" % model.__name__
        admin_class = admins.get(name, None)
        if admin_class is None:
            admin_class = type(
                "%sAdmin" % model.__name__,
                (admin.ModelAdmin,), {},
            )

        if admin_class.list_display == ('__str__',):
            admin_class.list_display = tuple(
                [f.name for f in model._meta.fields])

        additionals = getattr(admin_class, 'list_additionals', ())
        excludes = getattr(admin_class, 'list_excludes', ())
        admin_class.list_display = tuple(
            [n for n in admin_class.list_display
             if n not in excludes]) + additionals

        admin.site.register(model, admin_class)


class WpUsersAdmin(admin.ModelAdmin):
    search_fields = ('user_login', 'user_email', )
    date_hierarchy = 'user_registered'
    list_filter = ('user_status', )
    list_excludes = ('id', )


class WpUsermetaAdmin(admin.ModelAdmin):
    search_fields = ('user__user_login', )
    raw_id_fields = ('user', )
    list_filter = ('meta_key', )


class WpPostsAdmin(admin.ModelAdmin):
    date_hierarchy = 'post_modified'
    list_filter = ['post_type', 'post_mime_type', 'post_status', ]
    list_excludes = ['post_date_gmt', 'post_modified_gmt', ]


class WpOptionsAdmin(admin.ModelAdmin):
    list_filter = ['autoload', ]
    search_fields = ['option_name', 'option_value', ]

register(__name__, globals())
