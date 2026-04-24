from django.apps import AppConfig


class HubAuthConfig(AppConfig):  # type: ignore[misc]  # django.apps is untyped
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    # Label must differ from django.contrib.auth's "auth" label to avoid clash.
    label = "hub_auth"
    verbose_name = "Hub auth"
