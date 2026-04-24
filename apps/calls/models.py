# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class CallTemplates(models.Model):
    id = models.TextField(primary_key=True)
    call_type = models.TextField(unique=True)
    pre_call_prompt = models.TextField()
    coaching_prompt = models.TextField()
    post_call_prompt = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "call_templates"


class CallTranscripts(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    calendar_event_id = models.TextField(blank=True, null=True)
    call_type = models.TextField(blank=True, null=True)
    participants = models.JSONField(blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    action_items = models.JSONField(blank=True, null=True)
    follow_ups = models.JSONField(blank=True, null=True)
    sentiment = models.TextField(blank=True, null=True)
    coaching_notes = models.JSONField(blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True, null=True)
    processed = models.IntegerField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "call_transcripts"


class VoiceIntakes(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    user_email = models.TextField()
    transcript = models.TextField()
    intent = models.TextField()
    routed_to = models.JSONField(blank=True, null=True)
    target_person = models.TextField(blank=True, null=True)
    target_entity = models.TextField(blank=True, null=True)
    confirmation = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    result_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "voice_intakes"
