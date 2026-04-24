"""Base settings for the hub project.

Environment-specific variants live alongside this file (`dev.py`, `test.py`).
Future tickets will extend this module with middleware, auth, envelope renderer,
tenant/impersonation plumbing, and DRF config.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Overridden in dev / test
SECRET_KEY = "django-insecure-CHANGE-ME"
DEBUG = False
ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.common",
    "apps.auth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Hub tenant resolution from ?tenant=<id>. Runs after auth so views can
    # cross-check request.user against request.tenant_id if needed.
    "apps.common.middleware.tenant.TenantMiddleware",
    # Superadmin-only ?impersonate=<email>. Runs after auth + tenant so it can
    # check request.user.role and short-circuit with a 403 envelope response.
    "apps.common.middleware.impersonation.ImpersonationMiddleware",
    # x-xray-session passthrough + structured per-request log. Runs last so
    # the log record captures the final response status and duration.
    "apps.common.middleware.xray.XraySessionMiddleware",
]

ROOT_URLCONF = "hub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hub.wsgi.application"
ASGI_APPLICATION = "hub.asgi.application"

# Overridden in dev (postgres) once docker-compose lands in TKT-010.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK: dict[str, object] = {
    "DEFAULT_RENDERER_CLASSES": [
        "apps.common.renderers.HubJSONRenderer",
    ],
    "EXCEPTION_HANDLER": "apps.common.exceptions.hub_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.HubLimitPagination",
}

# Structured JSON logging for request records. TKT-071 adds a Grafana Cloud
# OTLP handler behind a TelemetrySink abstraction; until then, records go to
# stdout where the docker-compose log aggregator picks them up.
LOGGING: dict[str, object] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "hub_json": {
            "()": "apps.common.logging.JsonFormatter",
        },
    },
    "handlers": {
        "console_json": {
            "class": "logging.StreamHandler",
            "formatter": "hub_json",
        },
    },
    "loggers": {
        "hub.request": {
            "handlers": ["console_json"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
