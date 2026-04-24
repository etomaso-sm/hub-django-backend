from django.apps import AppConfig


class CrmConfig(AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.crm"
