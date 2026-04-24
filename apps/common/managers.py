"""Tenant-scoped manager for per-tenant models.

Any model with a `tenant_id` field and `managed=True` MUST use this manager
as its default manager. The system check in ``apps.common.checks`` enforces
this at startup.
"""

from typing import Any

from django.db import models

from apps.common.middleware.tenant import get_current_tenant


class TenantScopedManager(models.Manager):  # type: ignore[misc]
    """Auto-filter queries by the current tenant.

    Relies on the tenant contextvar populated by ``TenantMiddleware``. If the
    manager is used outside a tenant-aware context (e.g. shell, management
    command, Celery task without setup), ``get_current_tenant()`` raises
    ``TenantNotSetError`` — fail loudly instead of leaking across tenants.
    """

    def get_queryset(self) -> models.QuerySet[Any]:
        return super().get_queryset().filter(tenant_id=get_current_tenant())
