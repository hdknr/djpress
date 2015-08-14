from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import (
    ugettext_lazy as _,
)


class AppConfig(DjangoAppConfig):
    name = 'djpress'
    verbose_name = _("Djpress")

    def ready(self):
        import signals
