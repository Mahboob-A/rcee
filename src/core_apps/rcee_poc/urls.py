# urls.py

from django.urls import path
from core_apps.rcee_poc.views import execute_code

urlpatterns = [
    path("execute/", execute_code, name="execute_code"),
]
