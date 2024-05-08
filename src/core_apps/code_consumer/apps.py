from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CodeConsumerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.code_consumer"
    verbose_name = _("Code Consumer")
    verbose_name_plural = _("Code Consumers")
