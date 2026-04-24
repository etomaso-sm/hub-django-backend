from django.apps import AppConfig


class CommonConfig(AppConfig):  # type: ignore[misc]  # django.apps is untyped without django-stubs
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"
    label = "common"
