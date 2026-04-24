"""Local dev settings - loaded by default via manage.py."""

import os
from urllib.parse import urlparse

from hub.settings.base import *  # noqa: F401,F403

DEBUG = True
SECRET_KEY = "django-insecure-dev-key-only"
ALLOWED_HOSTS = ["*"]
DEV_BYPASS_AUTH_AS_EMAIL = os.getenv("DEV_BYPASS_AUTH_AS_EMAIL") or None

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or ""),
        }
    }
