# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class StreamEntries(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    hub_id = models.TextField()
    source_type = models.TextField()
    source_id = models.TextField(blank=True, null=True)
    agent_id = models.TextField(blank=True, null=True)
    user_email = models.TextField(blank=True, null=True)
    event_type = models.TextField()
    summary = models.TextField(blank=True, null=True)
    payload_json = models.JSONField(blank=True, null=True)
    visibility = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "stream_entries"
