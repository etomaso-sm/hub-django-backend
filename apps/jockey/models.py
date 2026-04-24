# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class BuildItems(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    type = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    severity = models.TextField()
    status = models.TextField()
    assigned_agent = models.TextField(blank=True, null=True)
    session_id = models.TextField(blank=True, null=True)
    created_by = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField()
    wave = models.TextField(blank=True, null=True)
    item_type = models.TextField(blank=True, null=True)
    project = models.TextField(blank=True, null=True)
    screenshot_url = models.TextField(blank=True, null=True)
    reporter_email = models.TextField(blank=True, null=True)
    fix_notes = models.TextField(blank=True, null=True)
    session_prompt = models.TextField(blank=True, null=True)
    qa_result = models.TextField(blank=True, null=True)
    page_url = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "build_items"


class BuildNotes(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    created_by = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField()

    class Meta:
        db_table = "build_notes"


class BuildTests(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    test_type = models.TextField()
    status = models.TextField()
    result_notes = models.TextField(blank=True, null=True)
    linked_build_item_id = models.TextField(blank=True, null=True)
    created_by = models.TextField()
    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField()

    class Meta:
        db_table = "build_tests"


class ClientJockeyConfigs(models.Model):
    id = models.TextField(primary_key=True)
    client_id = models.TextField()
    project_name = models.TextField(blank=True, null=True)
    tech_stack = models.JSONField(blank=True, null=True)
    conventions = models.TextField(blank=True, null=True)
    deploy_target = models.TextField(blank=True, null=True)
    repo_url = models.TextField(blank=True, null=True)
    total_sessions_planned = models.IntegerField(blank=True, null=True)
    total_sessions_completed = models.IntegerField(blank=True, null=True)
    total_cost_usd = models.FloatField(blank=True, null=True)
    revenue_monthly = models.FloatField(blank=True, null=True)
    margin_actual = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "client_jockey_configs"


class DeploymentGuards(models.Model):
    id = models.TextField(primary_key=True)
    session_id = models.TextField()
    file_path = models.TextField()
    guard_type = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "deployment_guards"


class JockeyDecisions(models.Model):
    id = models.TextField(primary_key=True)
    project_id = models.TextField()
    session_id = models.TextField(blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    options = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    assigned_to = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    decision = models.TextField(blank=True, null=True)
    decided_by = models.TextField(blank=True, null=True)
    decided_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "jockey_decisions"


class JockeyEvals(models.Model):
    id = models.TextField(primary_key=True)
    eval_date = models.TextField()
    type = models.TextField()
    findings = models.TextField()
    actions_taken = models.JSONField(blank=True, null=True)
    actions_pending = models.TextField(blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "jockey_evals"


class JockeyPatterns(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    source_project_id = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    description = models.TextField()
    pattern_content = models.TextField()
    adopted_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "jockey_patterns"


class JockeyRunnerConfig(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    runner_type = models.TextField(blank=True, null=True)
    repo_url = models.TextField(blank=True, null=True)
    github_app_installation_id = models.TextField(blank=True, null=True)
    deploy_target = models.TextField(blank=True, null=True)
    max_concurrent = models.IntegerField(blank=True, null=True)
    monthly_session_limit = models.IntegerField(blank=True, null=True)
    monthly_cost_limit_usd = models.FloatField(blank=True, null=True)
    api_key_source = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "jockey_runner_config"


class JockeySessions(models.Model):
    id = models.TextField(primary_key=True)
    project_id = models.TextField()
    title = models.TextField()
    status = models.TextField()
    automation_level = models.IntegerField(blank=True, null=True)
    operator_id = models.TextField(blank=True, null=True)
    prompt_template_version = models.TextField(blank=True, null=True)
    skills_loaded = models.TextField(blank=True, null=True)
    scope_files_planned = models.TextField(blank=True, null=True)
    scope_files_actual = models.TextField(blank=True, null=True)
    scope_violation = models.IntegerField(blank=True, null=True)
    verification_result = models.TextField(blank=True, null=True)
    verification_output = models.TextField(blank=True, null=True)
    token_usage = models.IntegerField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    error_class = models.TextField(blank=True, null=True)
    error_detail = models.TextField(blank=True, null=True)
    prompt_text = models.TextField(blank=True, null=True)
    session_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    deployed_at = models.DateTimeField(blank=True, null=True)
    delivery_target = models.TextField(blank=True, null=True)
    client_email = models.TextField(blank=True, null=True)
    execution_mode = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    deploy_approved_by = models.TextField(blank=True, null=True)
    deploy_approved_at = models.DateTimeField(blank=True, null=True)
    pr_url = models.TextField(blank=True, null=True)
    branch_name = models.TextField(blank=True, null=True)
    files_changed = models.IntegerField(blank=True, null=True)
    lines_added = models.IntegerField(blank=True, null=True)
    lines_removed = models.IntegerField(blank=True, null=True)
    commit_hash = models.TextField(blank=True, null=True)
    smoke_pass_count = models.IntegerField(blank=True, null=True)
    smoke_total_count = models.IntegerField(blank=True, null=True)
    chain_id = models.TextField(blank=True, null=True)
    chain_index = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "jockey_sessions"


class JockeySkills(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    project_id = models.TextField(blank=True, null=True)
    type = models.TextField()
    description = models.TextField(blank=True, null=True)
    file_path = models.TextField()
    success_rate = models.FloatField(blank=True, null=True)
    avg_duration_seconds = models.IntegerField(blank=True, null=True)
    total_uses = models.IntegerField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "jockey_skills"


class JockeyUsageLog(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    session_id = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    usage_type = models.TextField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "jockey_usage_log"
