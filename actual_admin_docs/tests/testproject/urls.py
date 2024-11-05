from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/docs/", include("actual_admin_docs.urls")),
    path("admin/", admin.site.urls),
]
