from django.apps import AppConfig


class HubAuthConfig(AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    label = "hub_auth"
    verbose_name = "Hub auth"
