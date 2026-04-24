# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ClientMigrations(models.Model):
    id = models.TextField(primary_key=True)
    client_id = models.TextField()
    client_name = models.TextField()
    current_revenue = models.IntegerField(blank=True, null=True)
    current_margin_pct = models.FloatField(blank=True, null=True)
    projected_margin_pct = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    readiness_score = models.FloatField(blank=True, null=True)
    complexity = models.TextField(blank=True, null=True)
    tech_stack = models.JSONField(blank=True, null=True)
    sessions_planned = models.IntegerField(blank=True, null=True)
    sessions_completed = models.IntegerField(blank=True, null=True)
    total_cost_usd = models.FloatField(blank=True, null=True)
    savings_monthly = models.FloatField(blank=True, null=True)
    approved_by = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "client_migrations"


class CompanyProfiles(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    team_size = models.IntegerField(blank=True, null=True)
    revenue = models.TextField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    agent_roster = models.TextField(blank=True, null=True)
    transformation_plan = models.TextField(blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    accent_color = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    conversation_policy = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "company_profiles"


class CompanyTypeTemplates(models.Model):
    id = models.TextField(primary_key=True)
    type_name = models.TextField()
    description = models.TextField(blank=True, null=True)
    default_agents = models.TextField()
    default_sidebar = models.TextField()
    onboarding_questions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "company_type_templates"


class SaasReplacementMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    tool_name = models.TextField()
    tool_aliases = models.JSONField(blank=True, null=True)
    category = models.TextField()
    hub_agent_id = models.TextField(blank=True, null=True)
    hub_agent_display = models.TextField(blank=True, null=True)
    avg_monthly_cost_cents = models.IntegerField(blank=True, null=True)
    business_types = models.JSONField(blank=True, null=True)
    active = models.IntegerField()

    class Meta:
        db_table = "saas_replacement_map"


class SaasTools(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    monthly_cost = models.FloatField(blank=True, null=True)
    hub_replacement = models.TextField(blank=True, null=True)
    hub_replacement_status = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "saas_tools"


class StorefrontAgentMap(models.Model):
    id = models.TextField(primary_key=True)
    storefront = models.ForeignKey("StorefrontBrands", models.DO_NOTHING)
    agent_config = models.ForeignKey("agents.AgentConfigs", models.DO_NOTHING)
    activation_rule = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    custom_prompt_override = models.TextField(blank=True, null=True)
    custom_data_tables = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_agent_map"
        unique_together = (("storefront", "agent_config"),)


class StorefrontApiKeys(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    key_hash = models.TextField()
    label = models.TextField(blank=True, null=True)
    scopes = models.JSONField(blank=True, null=True)
    rate_limit = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_api_keys"


class StorefrontBrands(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    slug = models.TextField(unique=True)
    name = models.TextField()
    domain = models.TextField(blank=True, null=True)
    tagline = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    accent_color = models.TextField(blank=True, null=True)
    bg_color = models.TextField(blank=True, null=True)
    logo_text = models.TextField(blank=True, null=True)
    pricing_json = models.JSONField(blank=True, null=True)
    scoping_intro = models.TextField(blank=True, null=True)
    cta_text = models.TextField(blank=True, null=True)
    features_json = models.JSONField(blank=True, null=True)
    legal_entity = models.TextField(blank=True, null=True)
    stripe_price_id = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    stripe_account_id = models.TextField(blank=True, null=True)
    connect_status = models.TextField(blank=True, null=True)
    connect_onboarded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_brands"


class StorefrontCustomers(models.Model):
    id = models.TextField(primary_key=True)
    brand_slug = models.TextField()
    email = models.TextField()
    name = models.TextField(blank=True, null=True)
    stripe_customer_id = models.TextField(blank=True, null=True)
    stripe_subscription_id = models.TextField(blank=True, null=True)
    product_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    mrr_cents = models.IntegerField(blank=True, null=True)
    provisioned_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    source = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "storefront_customers"
        unique_together = (("brand_slug", "email"),)


class StorefrontDeliverables(models.Model):
    id = models.TextField(primary_key=True)
    project_id = models.TextField()
    filename = models.TextField()
    file_type = models.TextField(blank=True, null=True)
    file_url = models.TextField(blank=True, null=True)
    size_bytes = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_deliverables"


class StorefrontEvaluations(models.Model):
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    evaluation_date = models.DateTimeField(blank=True, null=True)
    viability_score = models.FloatField(blank=True, null=True)
    automation_pct = models.IntegerField(blank=True, null=True)
    margin_estimate = models.FloatField(blank=True, null=True)
    acquisition_score = models.FloatField(blank=True, null=True)
    market_size = models.TextField(blank=True, null=True)
    competition = models.TextField(blank=True, null=True)
    pricing_model = models.TextField(blank=True, null=True)
    target_buyer = models.TextField(blank=True, null=True)
    strengths_json = models.JSONField(blank=True, null=True)
    risks_json = models.JSONField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    approved = models.IntegerField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    prd_generated = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_evaluations"


class StorefrontExperiments(models.Model):
    id = models.TextField(primary_key=True)
    brand_slug = models.TextField()
    experiment_type = models.TextField()
    variant_a = models.TextField()
    variant_b = models.TextField()
    metric = models.TextField()
    start_date = models.TextField(blank=True, null=True)
    end_date = models.TextField(blank=True, null=True)
    result_a = models.FloatField(blank=True, null=True)
    result_b = models.FloatField(blank=True, null=True)
    winner = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_experiments"


class StorefrontGtmConfigs(models.Model):
    id = models.TextField(primary_key=True)
    brand_slug = models.TextField()
    agent_id = models.TextField(blank=True, null=True)
    icp_json = models.JSONField()
    channels_json = models.JSONField(blank=True, null=True)
    messaging_json = models.JSONField(blank=True, null=True)
    kpis_json = models.JSONField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_gtm_configs"


class StorefrontLeads(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    email = models.TextField()
    company = models.TextField(blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    timeline = models.TextField(blank=True, null=True)
    budget_range = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    assigned_to = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "storefront_leads"


class StorefrontMetricsDaily(models.Model):
    id = models.TextField(primary_key=True)
    brand_slug = models.TextField()
    date = models.TextField()
    visits = models.IntegerField(blank=True, null=True)
    signups = models.IntegerField(blank=True, null=True)
    scans_started = models.IntegerField(blank=True, null=True)
    scans_completed = models.IntegerField(blank=True, null=True)
    subscriptions = models.IntegerField(blank=True, null=True)
    revenue_cents = models.IntegerField(blank=True, null=True)
    churn = models.IntegerField(blank=True, null=True)
    outbound_sent = models.IntegerField(blank=True, null=True)
    outbound_opens = models.IntegerField(blank=True, null=True)
    outbound_replies = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_metrics_daily"


class StorefrontOutboundSequences(models.Model):
    id = models.TextField(primary_key=True)
    brand_slug = models.TextField()
    sequence_name = models.TextField()
    steps_json = models.JSONField()
    target_persona = models.TextField(blank=True, null=True)
    tone = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_outbound_sequences"


class StorefrontPrds(models.Model):
    id = models.TextField(primary_key=True)
    evaluation_id = models.TextField(blank=True, null=True)
    agent_id = models.TextField()
    brand_name = models.TextField()
    brand_slug = models.TextField(blank=True, null=True)
    prd_json = models.JSONField()
    session_chain_json = models.JSONField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    approved = models.IntegerField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    jockey_project_id = models.TextField(blank=True, null=True)
    sessions_total = models.IntegerField(blank=True, null=True)
    sessions_completed = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_prds"


class StorefrontProducts(models.Model):
    id = models.TextField(primary_key=True)
    brand_slug = models.TextField()
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    price_cents = models.IntegerField()
    interval = models.TextField(blank=True, null=True)
    stripe_price_id = models.TextField(blank=True, null=True)
    stripe_product_id = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "storefront_products"


class StorefrontProjects(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    scope_id = models.TextField()
    agent_id = models.TextField()
    client_email = models.TextField(blank=True, null=True)
    client_name = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    tier = models.TextField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    deposit_paid = models.FloatField(blank=True, null=True)
    stripe_payment_id = models.TextField(blank=True, null=True)
    delivery_target = models.TextField(blank=True, null=True)
    phases_json = models.JSONField(blank=True, null=True)
    acceptance_status = models.TextField(blank=True, null=True)
    acceptance_deadline = models.TextField(blank=True, null=True)
    revision_count = models.IntegerField(blank=True, null=True)
    max_revisions = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    client_access_token = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "storefront_projects"


class StorefrontScopes(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    client_email = models.TextField(blank=True, null=True)
    client_name = models.TextField(blank=True, null=True)
    description = models.TextField()
    scope_doc = models.TextField(blank=True, null=True)
    pricing_estimate = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    files_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storefront_scopes"


class StudiosEngagements(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    client_id = models.TextField()
    client_name = models.TextField()
    engagement_name = models.TextField()
    delivery_method = models.TextField()
    monthly_revenue = models.FloatField()
    monthly_cogs = models.FloatField()
    headcount = models.FloatField(blank=True, null=True)
    jockey_sessions_month = models.IntegerField(blank=True, null=True)
    jockey_cost_month = models.FloatField(blank=True, null=True)
    status = models.TextField()
    start_date = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "studios_engagements"
