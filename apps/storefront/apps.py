from django.apps import AppConfig


class StorefrontConfig(AppConfig):  # type: ignore[misc]
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.storefront"
