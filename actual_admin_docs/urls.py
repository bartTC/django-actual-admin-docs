from django.urls import path

from .views import DocsView

app_name = "actual-admin-docs"

urlpatterns = [
    path("", DocsView.as_view(), name="index"),
    path("<path:page>", DocsView.as_view(), name="page"),
]
