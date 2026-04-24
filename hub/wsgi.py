"""WSGI config for hub project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings.dev")

application = get_wsgi_application()
