from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'pretix_paid_registration_email'
    verbose_name = 'pretix-paid-registration-email'

    class PretixPluginMeta:
        name = ugettext_lazy('pretix-paid-registration-email')
        author = 'Pratik Patel'
        description = ugettext_lazy('pretix-paid-registration-email')
        visible = True
        version = '1.0.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_paid_registration_email.PluginApp'
