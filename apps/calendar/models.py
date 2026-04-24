# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class CalendarEvents(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    connector_id = models.TextField()
    event_id = models.TextField(unique=True)
    title = models.TextField(blank=True, null=True)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    attendees = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    listener_processed = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "calendar_events"


class FilingDeadlines(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    entity = models.TextField()
    filing_type = models.TextField()
    description = models.TextField(blank=True, null=True)
    due_date = models.TextField()
    status = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    reminder_sent_30d = models.IntegerField(blank=True, null=True)
    reminder_sent_14d = models.IntegerField(blank=True, null=True)
    reminder_sent_7d = models.IntegerField(blank=True, null=True)
    reminder_sent_1d = models.IntegerField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "filing_deadlines"
