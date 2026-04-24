from django.apps import AppConfig


class BriefConfig(AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.brief"
