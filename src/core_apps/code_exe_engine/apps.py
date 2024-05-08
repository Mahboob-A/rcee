from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CodeExeEngineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.code_exe_engine"
    verbose_name = _("Code Execution Engine")
    verbose_name_plural = _("Code Execution Engine")
