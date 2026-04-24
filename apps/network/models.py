# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class NetworkConnections(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    owner_email = models.TextField()
    owner_name = models.TextField(blank=True, null=True)
    connection_name = models.TextField()
    connection_email = models.TextField(blank=True, null=True)
    connection_linkedin = models.TextField(blank=True, null=True)
    connection_company = models.TextField(blank=True, null=True)
    connection_title = models.TextField(blank=True, null=True)
    relationship = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "network_connections"
