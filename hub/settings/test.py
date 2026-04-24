"""Test settings - used by pytest (configured in pyproject.toml)."""

from hub.settings.base import *  # noqa: F401,F403

DEBUG = False
SECRET_KEY = "django-insecure-test-key"
ALLOWED_HOSTS = ["*"]
