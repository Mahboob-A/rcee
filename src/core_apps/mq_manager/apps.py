from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MqManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.mq_manager"
    verbose_name = _("MQ Manager")
    verbose_name_plural = _("MQ Managers")
