"""Root URL configuration for hub project.

Per-app URLconfs are included under `api/` starting at TKT-023 (core auth).
"""

from django.contrib import admin
from django.urls import path

from apps.common import smoke_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/_smoke/ping", smoke_views.ping),
]
