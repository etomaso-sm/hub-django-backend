from django.apps import AppConfig


class CommonConfig(AppConfig):  # type: ignore[misc]  # django.apps is untyped without django-stubs
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"
    label = "common"

    def ready(self) -> None:
        # Registering the module is enough — the @register() decorator in
        # apps.common.checks wires the check into Django's startup-time scan.
        from apps.common import checks  # noqa: F401
