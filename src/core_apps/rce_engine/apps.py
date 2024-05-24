from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RceEngineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.rce_engine"
    verbose_name = "RCE Engine"
    verbose_name_plural = "RCE Engines"
