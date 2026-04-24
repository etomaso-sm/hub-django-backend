# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class AgentWorkQueue(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    agent_id = models.TextField()
    action_type = models.TextField()
    payload = models.JSONField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "agent_work_queue"


class AutomationCoverage(models.Model):
    id = models.TextField(primary_key=True)
    process_name = models.TextField()
    description = models.TextField(blank=True, null=True)
    current_method = models.TextField(blank=True, null=True)
    hub_replacement = models.TextField(blank=True, null=True)
    hub_ready = models.IntegerField(blank=True, null=True)
    monthly_cost_manual = models.FloatField(blank=True, null=True)
    monthly_cost_hub = models.FloatField(blank=True, null=True)
    savings_monthly = models.FloatField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    assigned_to = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    activated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "automation_coverage"


class CardSnooze(models.Model):
    id = models.TextField(primary_key=True)
    card_id = models.TextField(blank=True, null=True)
    user_email = models.TextField(blank=True, null=True)
    snooze_until = models.DateTimeField(blank=True, null=True)
    dismissed = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "card_snooze"


class PartnerCommitments(models.Model):
    id = models.BigAutoField(primary_key=True)
    partner_email = models.TextField()
    commitment = models.TextField()
    source = models.TextField(blank=True, null=True)
    due_date = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    nudge_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "partner_commitments"


class ProjectDependencies(models.Model):
    id = models.TextField(primary_key=True)
    source_initiative_id = models.TextField()
    target_initiative_id = models.TextField()
    dependency_type = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "project_dependencies"


class RateLimits(models.Model):
    key = models.TextField(primary_key=True)
    count = models.IntegerField()
    window_start = models.DateTimeField()

    class Meta:
        db_table = "rate_limits"


class Tasks(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    title = models.TextField()
    owner = models.TextField()
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    initiative = models.ForeignKey("hub_app.Initiatives", models.DO_NOTHING, blank=True, null=True)
    priority = models.TextField()
    status = models.TextField()
    due_date = models.TextField(blank=True, null=True)
    source = models.TextField()
    source_agent = models.TextField(blank=True, null=True)
    requires_approval = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    chain_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tasks"


class WorkflowRuns(models.Model):
    id = models.TextField(primary_key=True)
    workflow_id = models.TextField()
    trigger_event = models.TextField(blank=True, null=True)
    actions_executed_json = models.JSONField(blank=True, null=True)
    status = models.TextField()
    error = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    workflow_type = models.TextField(blank=True, null=True)
    triggered_by = models.TextField(blank=True, null=True)
    steps = models.TextField(blank=True, null=True)
    current_step = models.IntegerField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "workflow_runs"


class Workflows(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    trigger_type = models.TextField()
    trigger_config_json = models.JSONField(blank=True, null=True)
    actions_json = models.JSONField(blank=True, null=True)
    status = models.TextField()
    created_by = models.TextField(blank=True, null=True)
    last_triggered_at = models.DateTimeField(blank=True, null=True)
    run_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "workflows"
