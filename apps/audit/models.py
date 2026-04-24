# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ActionAudit(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    card_id = models.TextField(blank=True, null=True)
    agent_id = models.TextField(blank=True, null=True)
    action_type = models.TextField(blank=True, null=True)
    action_label = models.TextField(blank=True, null=True)
    user_email = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "action_audit"


class AgentSuspensions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    reason = models.TextField()
    violation_id = models.TextField(blank=True, null=True)
    suspended_by = models.TextField()
    suspended_at = models.DateTimeField(blank=True, null=True)
    reinstated_by = models.TextField(blank=True, null=True)
    reinstated_at = models.DateTimeField(blank=True, null=True)
    reinstate_notes = models.TextField(blank=True, null=True)
    probation_until = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "agent_suspensions"


class AgentToolAudit(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    user_email = models.TextField(blank=True, null=True)
    tool_type = models.TextField()
    tool_name = models.TextField(blank=True, null=True)
    input_summary = models.TextField(blank=True, null=True)
    result_summary = models.TextField(blank=True, null=True)
    autonomy_level = models.IntegerField(blank=True, null=True)
    approved_by = models.TextField(blank=True, null=True)
    blocked_by = models.TextField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_tool_audit"


class AuditFindings(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    category = models.TextField()
    severity = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    line_number = models.IntegerField(blank=True, null=True)
    status = models.TextField()
    found_by = models.TextField(blank=True, null=True)
    fixed_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    resolved_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField()

    class Meta:
        db_table = "audit_findings"


class AuditRuns(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    run_type = models.TextField()
    findings_count = models.IntegerField(blank=True, null=True)
    critical_count = models.IntegerField(blank=True, null=True)
    warning_count = models.IntegerField(blank=True, null=True)
    info_count = models.IntegerField(blank=True, null=True)
    duration_ms = models.IntegerField(blank=True, null=True)
    triggered_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField()

    class Meta:
        db_table = "audit_runs"


class BugReports(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField(blank=True, null=True)
    page = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "bug_reports"


class Events(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField()
    entity_id = models.TextField(blank=True, null=True)
    actor = models.TextField()
    target_type = models.TextField(blank=True, null=True)
    target_id = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "events"


class PlatformPolicies(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    policy_type = models.TextField()
    version = models.TextField()
    title = models.TextField()
    content = models.TextField()
    effective_date = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "platform_policies"


class PlatformViolations(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    entity_type = models.TextField()
    entity_id = models.TextField()
    violation_type = models.TextField()
    severity = models.TextField()
    description = models.TextField()
    evidence = models.TextField(blank=True, null=True)
    policy_reference = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    resolved_by = models.TextField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "platform_violations"


class SecurityControls(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    category = models.TextField()
    control_name = models.TextField()
    status = models.TextField(blank=True, null=True)
    evidence = models.TextField(blank=True, null=True)
    last_verified = models.TextField(blank=True, null=True)
    responsible = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "security_controls"
