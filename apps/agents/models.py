# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class AgentAccountabilityChain(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    chain_id = models.TextField()
    sequence_number = models.IntegerField()
    agent_id = models.TextField()
    action_type = models.TextField()
    action_description = models.TextField(blank=True, null=True)
    input_summary = models.TextField(blank=True, null=True)
    output_summary = models.TextField(blank=True, null=True)
    data_tables_accessed = models.TextField(blank=True, null=True)
    autonomy_level = models.IntegerField(blank=True, null=True)
    delegated_to = models.TextField(blank=True, null=True)
    delegated_reason = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    duration_ms = models.IntegerField(blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_accountability_chain"


class AgentActions(models.Model):
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    user_email = models.TextField()
    action_type = models.TextField()
    target_table = models.TextField()
    target_id = models.TextField(blank=True, null=True)
    operation = models.TextField()
    sql_statement = models.TextField()
    description = models.TextField()
    autonomy_level = models.IntegerField()
    status = models.TextField()
    approved_by = models.TextField(blank=True, null=True)
    executed_at = models.DateTimeField(blank=True, null=True)
    error_detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    prompt_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "agent_actions"
        unique_together = (("agent_id", "target_table", "target_id", "operation"),)


class AgentConfigs(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField(blank=True, null=True)
    system_prompt = models.TextField()
    data_tables = models.JSONField(blank=True, null=True)
    tools = models.JSONField(blank=True, null=True)
    trigger_schedule = models.TextField(blank=True, null=True)
    sidebar_section = models.TextField(blank=True, null=True)
    default_autonomy_level = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tier = models.IntegerField(blank=True, null=True)
    display_name = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    works_with = models.JSONField(blank=True, null=True)
    depends_on = models.JSONField(blank=True, null=True)
    serves_roles = models.JSONField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    productizable = models.IntegerField(blank=True, null=True)
    product_category = models.TextField(blank=True, null=True)
    status_summary = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    max_daily_tokens = models.IntegerField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    mcp_permissions = models.JSONField(blank=True, null=True)
    thinking_budget = models.IntegerField(blank=True, null=True)
    sidebar_sections = models.JSONField(blank=True, null=True)
    required_tools = models.JSONField(blank=True, null=True)
    max_access_tier = models.IntegerField(blank=True, null=True)
    knowledge_domains = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "agent_configs"


class AgentConversations(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    user_email = models.TextField()
    title = models.TextField(blank=True, null=True)
    visibility = models.TextField(blank=True, null=True)
    last_message_at = models.DateTimeField(blank=True, null=True)
    message_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_conversations"


class AgentInstances(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    template = models.ForeignKey("AgentTemplates", models.DO_NOTHING)
    tenant_id = models.TextField()
    agent_config_id = models.TextField(blank=True, null=True)
    prompt_overrides = models.TextField(blank=True, null=True)
    connected_data_sources = models.JSONField(blank=True, null=True)
    custom_sections = models.JSONField(blank=True, null=True)
    autonomy_level = models.IntegerField(blank=True, null=True)
    pinned_version = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_instances"
        unique_together = (("tenant_id", "template"),)


class AgentMemory(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    agent = models.ForeignKey(AgentConfigs, models.DO_NOTHING)
    entity_type = models.TextField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    memory_type = models.TextField()
    content = models.TextField()
    confidence = models.FloatField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    user_email = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "agent_memory"


class AgentModelUsage(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    agent_name = models.TextField(blank=True, null=True)
    model = models.TextField()
    tokens_in = models.IntegerField(blank=True, null=True)
    tokens_out = models.IntegerField(blank=True, null=True)
    cache_read_tokens = models.IntegerField(blank=True, null=True)
    cache_write_tokens = models.IntegerField(blank=True, null=True)
    latency_ms = models.IntegerField(blank=True, null=True)
    cost_cents = models.FloatField(blank=True, null=True)
    success = models.IntegerField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    trigger = models.TextField(blank=True, null=True)
    user_email = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    provider = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "agent_model_usage"


class AgentPatterns(models.Model):
    id = models.TextField(primary_key=True)
    pattern_type = models.TextField()
    source_agent = models.TextField(blank=True, null=True)
    description = models.TextField()
    frequency = models.IntegerField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    suggestion = models.TextField(blank=True, null=True)
    applied = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "agent_patterns"


class AgentProposals(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    type = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    proposed_by = models.TextField()
    status = models.TextField()
    source_conversation_id = models.TextField(blank=True, null=True)
    reviewed_by = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "agent_proposals"


class AgentRoleTemplates(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    slug = models.TextField(unique=True)
    description = models.TextField(blank=True, null=True)
    sidebar_items = models.JSONField()
    brief_agents = models.JSONField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_role_templates"


class AgentRuns(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    agent = models.ForeignKey(AgentConfigs, models.DO_NOTHING)
    user_email = models.TextField()
    trigger = models.TextField()
    input = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    recommendations = models.JSONField(blank=True, null=True)
    actions_taken = models.JSONField(blank=True, null=True)
    autonomy_level_used = models.IntegerField(blank=True, null=True)
    user_feedback = models.TextField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    duration_ms = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    action_taken = models.IntegerField(blank=True, null=True)
    awaiting_approval = models.IntegerField(blank=True, null=True)
    actioned_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    undoable = models.IntegerField(blank=True, null=True)
    actions_json = models.JSONField(blank=True, null=True)
    autonomy_level = models.IntegerField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    conversation_id = models.TextField(blank=True, null=True)
    visibility = models.TextField(blank=True, null=True)
    snoozed_until = models.DateTimeField(blank=True, null=True)
    dismissed = models.IntegerField(blank=True, null=True)
    artifact_id = models.TextField(blank=True, null=True)
    compliance_flags = models.JSONField(blank=True, null=True)
    attachments_json = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "agent_runs"


class AgentTemplates(models.Model):
    id = models.TextField(primary_key=True)
    slug = models.TextField(unique=True)
    display_name = models.TextField()
    category = models.TextField(blank=True, null=True)
    skill_prompt = models.TextField()
    data_needs = models.JSONField(blank=True, null=True)
    required_connectors = models.JSONField(blank=True, null=True)
    tools = models.JSONField(blank=True, null=True)
    sections = models.JSONField(blank=True, null=True)
    domain_keywords = models.JSONField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    default_autonomy_level = models.IntegerField(blank=True, null=True)
    jockey_capable = models.IntegerField(blank=True, null=True)
    brain_context = models.IntegerField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    changelog = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_templates"


class AgentTransactions(models.Model):
    id = models.TextField(primary_key=True)
    source_hub_id = models.TextField(blank=True, null=True)
    source_agent_id = models.TextField(blank=True, null=True)
    target_storefront = models.TextField()
    tool_name = models.TextField()
    request_json = models.JSONField(blank=True, null=True)
    response_json = models.JSONField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    latency_ms = models.IntegerField(blank=True, null=True)
    revenue_cents = models.IntegerField(blank=True, null=True)
    platform_fee_cents = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_transactions"


class AgentTriggerChains(models.Model):
    id = models.TextField(primary_key=True)
    source_agent = models.TextField()
    trigger_event = models.TextField()
    target_agent = models.TextField()
    target_trigger = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "agent_trigger_chains"


class AutonomyScores(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    agent = models.ForeignKey(AgentConfigs, models.DO_NOTHING)
    action_type = models.TextField()
    user_email = models.TextField()
    total_actions = models.IntegerField(blank=True, null=True)
    approved_unchanged = models.IntegerField(blank=True, null=True)
    approved_edited = models.IntegerField(blank=True, null=True)
    rejected = models.IntegerField(blank=True, null=True)
    avg_edit_distance = models.FloatField(blank=True, null=True)
    current_level = models.IntegerField(blank=True, null=True)
    level_up_eligible = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "autonomy_scores"
        unique_together = (("agent", "action_type", "user_email"),)


class CrackedFindings(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    category = models.TextField(blank=True, null=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    cost_benefit = models.TextField(blank=True, null=True)
    impact_score = models.FloatField(blank=True, null=True)
    auto_eligible = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "cracked_findings"


class CrackedProposals(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    finding_id = models.TextField(blank=True, null=True)
    proposal_type = models.TextField(blank=True, null=True)
    target_agent_id = models.TextField(blank=True, null=True)
    change_description = models.TextField(blank=True, null=True)
    risk_level = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "cracked_proposals"


class EventTriggers(models.Model):
    id = models.TextField(primary_key=True)
    event_type = models.TextField()
    agent_id = models.TextField()
    filter_json = models.JSONField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "event_triggers"


class EvolverAudits(models.Model):
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    status = models.TextField()
    findings = models.TextField(blank=True, null=True)
    recommended_prompt = models.TextField(blank=True, null=True)
    recommended_action = models.TextField(blank=True, null=True)
    severity = models.TextField(blank=True, null=True)
    applied = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "evolver_audits"


class EvolverRuns(models.Model):
    id = models.TextField(primary_key=True)
    agents_audited = models.IntegerField(blank=True, null=True)
    stale_count = models.IntegerField(blank=True, null=True)
    dormant_count = models.IntegerField(blank=True, null=True)
    missing_count = models.IntegerField(blank=True, null=True)
    current_count = models.IntegerField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "evolver_runs"
