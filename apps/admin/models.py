# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class DeployVerifications(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    git_sha = models.TextField(blank=True, null=True)
    session_id = models.TextField(blank=True, null=True)
    triggered_by = models.TextField(blank=True, null=True)
    total_checks = models.IntegerField(blank=True, null=True)
    passed = models.IntegerField(blank=True, null=True)
    failed = models.IntegerField(blank=True, null=True)
    overall = models.TextField(blank=True, null=True)
    results_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "deploy_verifications"


class ProviderHealth(models.Model):
    provider = models.TextField(primary_key=True)
    status = models.TextField(blank=True, null=True)
    last_check = models.TextField(blank=True, null=True)
    last_success = models.TextField(blank=True, null=True)
    last_error = models.TextField(blank=True, null=True)
    error_rate_1h = models.FloatField(blank=True, null=True)
    latency_p95_ms = models.IntegerField(blank=True, null=True)
    consecutive_failures = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "provider_health"


class ReleaseNotes(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    session_id = models.TextField(blank=True, null=True)
    title = models.TextField()
    summary = models.TextField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    commit_hash = models.TextField(blank=True, null=True)
    commit_date = models.TextField(blank=True, null=True)
    files_changed = models.IntegerField(blank=True, null=True)
    chain = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "release_notes"


class RetryQueue(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    user_email = models.TextField()
    prompt = models.TextField()
    conversation_id = models.TextField(blank=True, null=True)
    original_error = models.TextField(blank=True, null=True)
    retry_count = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "retry_queue"


class StatusChecks(models.Model):
    id = models.TextField(primary_key=True)
    service = models.TextField()
    endpoint = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    response_ms = models.IntegerField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    checked_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "status_checks"


class StatusIncidents(models.Model):
    id = models.TextField(primary_key=True)
    service = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    severity = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "status_incidents"
