# urls.py

from django.urls import path
from core_apps.rcee_poc.views import CodeSubmitSimpleImplementation, CodeSubmitRobustAPI

urlpatterns = [
    path(
        "simple-execute/",
        CodeSubmitSimpleImplementation.as_view(),
        name="simple_execute_code",
    ),
    path("robust-execute/", CodeSubmitRobustAPI.as_view(), name="robust_execute_code"),
]
