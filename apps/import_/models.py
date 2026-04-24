# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class EnrichmentLog(models.Model):
    id = models.TextField(primary_key=True)
    contact_id = models.TextField(blank=True, null=True)
    company_id = models.TextField(blank=True, null=True)
    source = models.TextField()
    request_type = models.TextField(blank=True, null=True)
    response_status = models.IntegerField(blank=True, null=True)
    fields_filled = models.TextField(blank=True, null=True)
    fields_skipped = models.TextField(blank=True, null=True)
    cost_credits = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "enrichment_log"


class ImportBatches(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    source = models.TextField()
    imported_by = models.TextField()
    status = models.TextField()
    total_records = models.IntegerField(blank=True, null=True)
    valid_records = models.IntegerField(blank=True, null=True)
    imported_records = models.IntegerField(blank=True, null=True)
    merged_records = models.IntegerField(blank=True, null=True)
    dropped_records = models.IntegerField(blank=True, null=True)
    enriched_records = models.IntegerField(blank=True, null=True)
    error_details = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "import_batches"


class ImportLinks(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    token = models.TextField(unique=True)
    created_by = models.TextField()
    label = models.TextField(blank=True, null=True)
    scopes = models.JSONField(blank=True, null=True)
    max_uses = models.IntegerField(blank=True, null=True)
    use_count = models.IntegerField(blank=True, null=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(blank=True, null=True)
    ip_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "import_links"


class IngestionPreviews(models.Model):
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    user_email = models.TextField()
    filename = models.TextField(blank=True, null=True)
    file_type = models.TextField(blank=True, null=True)
    status = models.TextField()
    proposed_changes = models.TextField()
    summary = models.TextField(blank=True, null=True)
    row_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    applied_at = models.DateTimeField(blank=True, null=True)
    applied_by = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "ingestion_previews"
