# urls.py

from django.urls import path
from core_apps.rce_engine.views import CodeSubmitAPI


urlpatterns = [
    path("execute/", CodeSubmitAPI.as_view(), name="execute_code"),
]
