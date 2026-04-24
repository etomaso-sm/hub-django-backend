from django.apps import AppConfig


class ImportConfig(AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.import_"
    label = "import_app"
    verbose_name = "Import"
