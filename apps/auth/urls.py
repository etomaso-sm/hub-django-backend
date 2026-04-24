"""Core auth URL routes for TKT-023."""

from django.urls import path

from apps.auth import views

urlpatterns = [
    path("auth/login", views.login),
    path("auth/session", views.auth_session),
    path("me", views.me),
    path("signup", views.signup),
    path("tenants", views.tenants),
    path("hub/list", views.hub_list),
    path("hub/switch", views.hub_switch),
    path("hub/current", views.hub_current),
]
