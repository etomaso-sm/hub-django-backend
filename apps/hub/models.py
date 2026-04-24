# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ClientContacts(models.Model):
    id = models.TextField(primary_key=True)
    client = models.ForeignKey("Clients", models.DO_NOTHING)
    name = models.TextField()
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    is_primary = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "client_contacts"


class Clients(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    entity = models.ForeignKey("Entities", models.DO_NOTHING)
    owner = models.TextField()
    status = models.TextField()
    health = models.TextField()
    monthly_value = models.FloatField(blank=True, null=True)
    margin_pct = models.FloatField(blank=True, null=True)
    renewal_date = models.TextField(blank=True, null=True)
    last_touch = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_date = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    stripe_customer_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "clients"


class Deals(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    entity = models.ForeignKey("Entities", models.DO_NOTHING)
    owner = models.TextField()
    type = models.TextField(blank=True, null=True)
    stage = models.TextField()
    amount = models.FloatField(blank=True, null=True)
    probability = models.FloatField(blank=True, null=True)
    close_date = models.TextField(blank=True, null=True)
    counterparty = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "deals"


class Entities(models.Model):
    id = models.TextField(primary_key=True)
    legal_name = models.TextField()
    type = models.TextField()
    jurisdiction = models.TextField(blank=True, null=True)
    parent_entity = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    status = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "entities"


class EntityStatus(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    entity_name = models.TextField()
    entity_type = models.TextField()
    owner = models.TextField()
    cash_position = models.FloatField(blank=True, null=True)
    monthly_burn = models.FloatField(blank=True, null=True)
    runway_months = models.FloatField(blank=True, null=True)
    status = models.TextField()
    health = models.TextField()
    current_milestone = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_owner = models.TextField(blank=True, null=True)
    blockers = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "entity_status"


class HubEvents(models.Model):
    id = models.TextField(primary_key=True)
    event_type = models.TextField()
    actor_type = models.TextField()
    actor_id = models.TextField()
    entity_type = models.TextField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "hub_events"


class HubFeedback(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField()
    agent_id = models.TextField(blank=True, null=True)
    run_id = models.TextField(blank=True, null=True)
    user_email = models.TextField()
    content = models.TextField(blank=True, null=True)
    agent_response = models.TextField(blank=True, null=True)
    data_context = models.TextField(blank=True, null=True)
    status = models.TextField()
    resolved_by = models.TextField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "hub_feedback"


class HubRegistry(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    hostname = models.TextField()
    db_binding = models.TextField()
    db_id = models.TextField(blank=True, null=True)
    owner_email = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "hub_registry"


class HubRelationships(models.Model):
    id = models.TextField(primary_key=True)
    parent_tenant_id = models.TextField()
    child_tenant_id = models.TextField()
    relationship_type = models.TextField(blank=True, null=True)
    permissions_json = models.JSONField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "hub_relationships"
        unique_together = (("parent_tenant_id", "child_tenant_id"),)


class HubRelays(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    from_email = models.TextField()
    to_email = models.TextField()
    subject = models.TextField()
    context = models.TextField(blank=True, null=True)
    source_agent_id = models.TextField(blank=True, null=True)
    source_conversation_id = models.TextField(blank=True, null=True)
    source_run_id = models.TextField(blank=True, null=True)
    response_conversation_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    response_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    relay_type = models.TextField(blank=True, null=True)
    thread_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "hub_relays"


class Initiatives(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    entity = models.ForeignKey(Entities, models.DO_NOTHING)
    division = models.TextField(blank=True, null=True)
    owner = models.TextField()
    status = models.TextField()
    health = models.TextField()
    current_milestone = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_date = models.TextField(blank=True, null=True)
    target_date = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    labs_visible = models.IntegerField(blank=True, null=True)
    labs_stage = models.TextField(blank=True, null=True)
    labs_section = models.TextField(blank=True, null=True)
    labs_tagline = models.TextField(blank=True, null=True)
    labs_description = models.TextField(blank=True, null=True)
    labs_icon = models.TextField(blank=True, null=True)
    labs_color = models.TextField(blank=True, null=True)
    labs_url = models.TextField(blank=True, null=True)
    labs_waitlist_url = models.TextField(blank=True, null=True)
    labs_demo_type = models.TextField(blank=True, null=True)
    labs_demo_source = models.TextField(blank=True, null=True)
    labs_sort_order = models.IntegerField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "initiatives"


class Milestones(models.Model):
    id = models.TextField(primary_key=True)
    initiative = models.ForeignKey(Initiatives, models.DO_NOTHING)
    name = models.TextField()
    status = models.TextField()
    due_date = models.TextField(blank=True, null=True)
    completed_date = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "milestones"


class Notes(models.Model):
    id = models.TextField(primary_key=True)
    target_type = models.TextField()
    target_id = models.TextField()
    author = models.TextField()
    content = models.TextField()
    is_private = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "notes"


class PortalActivityLog(models.Model):
    id = models.TextField(primary_key=True)
    investor_profile_id = models.TextField()
    action = models.TextField()
    detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "portal_activity_log"


class PortfolioCompanies(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    type = models.TextField()
    sector = models.TextField(blank=True, null=True)
    stage = models.TextField(blank=True, null=True)
    founded = models.TextField(blank=True, null=True)
    sprint_investment = models.IntegerField(blank=True, null=True)
    sprint_ownership_pct = models.FloatField(blank=True, null=True)
    sprint_equity_pct = models.FloatField(blank=True, null=True)
    cost_basis = models.IntegerField(blank=True, null=True)
    current_valuation = models.IntegerField(blank=True, null=True)
    sprint_position_value = models.IntegerField(blank=True, null=True)
    mrr = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    milestone = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    carta_fund_id = models.TextField(blank=True, null=True)
    last_valuation_date = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "portfolio_companies"


class TeamSignalHistory(models.Model):
    id = models.TextField(primary_key=True)
    person_email = models.TextField()
    date = models.TextField()
    signal = models.TextField()
    metrics_json = models.JSONField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "team_signal_history"
        unique_together = (("person_email", "date"),)


class TeamSignals(models.Model):
    id = models.TextField(primary_key=True)
    person_email = models.TextField()
    period = models.TextField()
    signal = models.TextField()
    signal_color = models.TextField()
    summary = models.TextField(blank=True, null=True)
    slack_activity_trend = models.FloatField(blank=True, null=True)
    last_project_update_days = models.IntegerField(blank=True, null=True)
    last_client_touch_days = models.IntegerField(blank=True, null=True)
    tasks_completed_this_week = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "team_signals"
