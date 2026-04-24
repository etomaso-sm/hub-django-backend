"""Root URL configuration for hub project.

Per-app URLconfs are included under `api/` starting at TKT-023 (core auth).
For now only the admin route is registered.
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
