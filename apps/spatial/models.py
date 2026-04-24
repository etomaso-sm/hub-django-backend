# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class CommsMessages(models.Model):
    id = models.TextField(primary_key=True)
    thread_id = models.TextField()
    sender_user_id = models.TextField(blank=True, null=True)
    sender_name = models.TextField()
    sender_type = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "comms_messages"


class CommsThreads(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField()
    title = models.TextField(blank=True, null=True)
    pinned = models.IntegerField()
    status = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    target_investors = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "comms_threads"


class SharedThreads(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    conversation_id = models.TextField()
    agent_id = models.TextField(blank=True, null=True)
    shared_by = models.TextField()
    shared_with = models.TextField()
    message_id = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "shared_threads"


class Threads(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField(blank=True, null=True)
    user_email = models.TextField()
    participants = models.JSONField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    visibility = models.TextField(blank=True, null=True)
    thread_type = models.TextField(blank=True, null=True)
    last_message_at = models.DateTimeField(blank=True, null=True)
    message_count = models.IntegerField(blank=True, null=True)
    agents_json = models.JSONField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cross_hub = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "threads"


class UserPresence(models.Model):
    objects = TenantScopedManager()
    user_email = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    last_active_at = models.DateTimeField()
    current_agent_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_presence"
