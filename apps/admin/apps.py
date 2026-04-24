from django.apps import AppConfig


class HubAdminConfig(AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.admin"
    label = "hub_admin"
    verbose_name = "Hub admin"
