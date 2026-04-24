# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class Approvals(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    type = models.TextField()
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    source_agent = models.TextField(blank=True, null=True)
    requested_by = models.TextField()
    assigned_to = models.TextField()
    risk_level = models.TextField()
    summary = models.TextField()
    detail = models.TextField(blank=True, null=True)
    status = models.TextField()
    decided_at = models.DateTimeField(blank=True, null=True)
    decided_by = models.TextField(blank=True, null=True)
    decision_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "approvals"


class Decisions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    title = models.TextField()
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    owners = models.TextField()
    decision_text = models.TextField()
    options_considered = models.TextField(blank=True, null=True)
    rationale = models.TextField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    follow_ups = models.JSONField(blank=True, null=True)
    sources = models.TextField(blank=True, null=True)
    status = models.TextField()
    decided_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "decisions"


class Documents(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    category = models.TextField()
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    owner = models.TextField()
    status = models.TextField()
    doc_url = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_date = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "documents"


class Governance(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    type = models.TextField()
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    owner = models.TextField()
    status = models.TextField()
    due_date = models.TextField(blank=True, null=True)
    completed_date = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "governance"


class LegalMatters(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    matter_type = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    status = models.TextField()
    priority = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    counsel = models.TextField(blank=True, null=True)
    deadline = models.TextField(blank=True, null=True)
    decided_date = models.TextField(blank=True, null=True)
    decided_by = models.TextField(blank=True, null=True)
    decision_summary = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    related_entity = models.TextField(blank=True, null=True)
    related_matter_id = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "legal_matters"
