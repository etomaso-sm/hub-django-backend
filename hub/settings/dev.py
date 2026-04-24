"""Local dev settings - loaded by default via manage.py."""

from hub.settings.base import *  # noqa: F401,F403

DEBUG = True
SECRET_KEY = "django-insecure-dev-key-only"
ALLOWED_HOSTS = ["*"]
