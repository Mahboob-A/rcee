from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RceePocConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.rcee_poc"
    verbose_name = "RCEE POC"
    verbose_name_plural = "RCEE POCs"
