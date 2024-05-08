from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResultProducerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.result_producer"
    verbose_name = _("Result Producer")
    verbose_name_plural = _("Result Producers")
