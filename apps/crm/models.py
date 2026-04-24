# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class CadenceLog(models.Model):
    id = models.TextField(primary_key=True)
    sequence_id = models.TextField()
    step_number = models.IntegerField()
    action = models.TextField()
    email_id = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "cadence_log"


class CadenceTemplates(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    name = models.TextField()
    steps_json = models.JSONField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "cadence_templates"


class Candidates(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    role_title = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    stage = models.TextField()
    source = models.TextField(blank=True, null=True)
    resume_url = models.TextField(blank=True, null=True)
    linkedin_url = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    jockey_score = models.IntegerField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "candidates"


class CommunicationQueue(models.Model):
    id = models.TextField(primary_key=True)
    source = models.TextField()
    source_id = models.TextField(blank=True, null=True)
    from_address = models.TextField(blank=True, null=True)
    from_name = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    preview = models.TextField(blank=True, null=True)
    urgency = models.TextField(blank=True, null=True)
    routed_to = models.JSONField(blank=True, null=True)
    classification = models.JSONField(blank=True, null=True)
    processed = models.IntegerField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    processed_by = models.TextField(blank=True, null=True)
    source_channel = models.TextField(blank=True, null=True)
    source_ts = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "communication_queue"


class CompetitorDomains(models.Model):
    domain = models.TextField(primary_key=True)
    company_name = models.TextField(blank=True, null=True)
    added_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "competitor_domains"


class CrmActivities(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    company_id = models.TextField(blank=True, null=True)
    contact_id = models.TextField(blank=True, null=True)
    activity_type = models.TextField()
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source_table = models.TextField(blank=True, null=True)
    source_id = models.TextField(blank=True, null=True)
    agent_id = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "crm_activities"


class CrmCompanies(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    name = models.TextField()
    domain = models.TextField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    revenue_range = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    company_type = models.TextField()
    relationship_types = models.JSONField(blank=True, null=True)
    hub_instance_url = models.TextField(blank=True, null=True)
    storefront_ids = models.JSONField(blank=True, null=True)
    si_entity_id = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    billing_email = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    health_score = models.IntegerField(blank=True, null=True)
    engagement_score = models.FloatField(blank=True, null=True)
    close_id = models.TextField(blank=True, null=True)
    close_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    import_batch_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "crm_companies"


class CrmContacts(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    company_id = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    contact_type = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_contact_id = models.TextField(blank=True, null=True)
    source_artifact_id = models.TextField(blank=True, null=True)
    investor_profile_id = models.TextField(blank=True, null=True)
    pipeline_stage = models.TextField(blank=True, null=True)
    funnel_stage = models.TextField(blank=True, null=True)
    engagement_score = models.FloatField(blank=True, null=True)
    last_engagement_at = models.DateTimeField(blank=True, null=True)
    enrichment_status = models.TextField(blank=True, null=True)
    enrichment_data = models.JSONField(blank=True, null=True)
    linkedin_url = models.TextField(blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    close_lead_id = models.TextField(blank=True, null=True)
    close_contact_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    import_batch_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "crm_contacts"


class CrmRelationships(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    from_company_id = models.TextField()
    to_company_id = models.TextField()
    relationship_type = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "crm_relationships"


class CrmSignalDismissals(models.Model):
    id = models.TextField(primary_key=True)
    signal_key = models.TextField()
    user_email = models.TextField()
    action = models.TextField(blank=True, null=True)
    snooze_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "crm_signal_dismissals"


class EmailClassifications(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    email_id = models.TextField(blank=True, null=True)
    from_addr = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    classification = models.TextField()
    confidence = models.FloatField(blank=True, null=True)
    signals_json = models.JSONField(blank=True, null=True)
    user_override = models.TextField(blank=True, null=True)
    overridden_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "email_classifications"


class EmailThreads(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    gmail_thread_id = models.TextField()
    subject = models.TextField(blank=True, null=True)
    participants = models.JSONField(blank=True, null=True)
    last_message_at = models.DateTimeField(blank=True, null=True)
    message_count = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    assigned_agent = models.TextField(blank=True, null=True)
    assigned_user = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "email_threads"
        unique_together = (("gmail_thread_id", "tenant_id"),)


class Emails(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    subject = models.TextField(blank=True, null=True)
    from_addr = models.TextField(blank=True, null=True)
    to_addr = models.TextField(blank=True, null=True)
    snippet = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)
    labels = models.TextField(blank=True, null=True)
    highlight = models.IntegerField(blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    gmail_message_id = models.TextField(blank=True, null=True)
    gmail_thread_id = models.TextField(blank=True, null=True)
    reply_status = models.TextField(blank=True, null=True)
    replied_by = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    outbound_email_id = models.TextField(blank=True, null=True)
    listener_processed = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "emails"


class Investors(models.Model):
    id = models.TextField(primary_key=True)
    pipeline_type = models.TextField()
    name = models.TextField()
    firm = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    owner = models.TextField()
    stage = models.TextField()
    persona = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    last_touch = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_date = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    investor_profile_id = models.TextField(blank=True, null=True)
    crm_contact_id = models.TextField(blank=True, null=True)
    crm_company_id = models.TextField(blank=True, null=True)
    pipeline_deal_id = models.TextField(blank=True, null=True)
    raise_id = models.TextField(blank=True, null=True)
    engagement_score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "investors"


class OutboundMessages(models.Model):
    id = models.TextField(primary_key=True)
    sequence = models.ForeignKey("OutboundSequences", models.DO_NOTHING)
    step = models.IntegerField()
    channel = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    opened_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "outbound_messages"


class OutboundSequences(models.Model):
    id = models.TextField(primary_key=True)
    prospect_id = models.TextField()
    prospect_name = models.TextField(blank=True, null=True)
    prospect_company = models.TextField(blank=True, null=True)
    prospect_email = models.TextField(blank=True, null=True)
    prospect_data = models.JSONField(blank=True, null=True)
    icp_score = models.FloatField(blank=True, null=True)
    sequence_step = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)
    last_response_at = models.DateTimeField(blank=True, null=True)
    engagement_score = models.FloatField(blank=True, null=True)
    qualified = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content_type = models.TextField(blank=True, null=True)
    artifact_id = models.TextField(blank=True, null=True)
    tracked_url = models.TextField(blank=True, null=True)
    source_agent_id = models.TextField(blank=True, null=True)
    page_slug = models.TextField(blank=True, null=True)
    max_scroll = models.IntegerField(blank=True, null=True)
    total_seconds = models.IntegerField(blank=True, null=True)
    visit_count = models.IntegerField(blank=True, null=True)
    forwarded_to = models.TextField(blank=True, null=True)
    source_sequence_id = models.TextField(blank=True, null=True)
    source_type = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "outbound_sequences"


class OutboundSlackMessages(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    channel = models.TextField()
    channel_name = models.TextField(blank=True, null=True)
    text = models.TextField()
    thread_ts = models.TextField(blank=True, null=True)
    status = models.TextField()
    approved_by = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    message_ts = models.TextField(blank=True, null=True)
    agent_id = models.TextField(blank=True, null=True)
    run_id = models.TextField(blank=True, null=True)
    triggered_by = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "outbound_slack_messages"


class PipelineDeals(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    pipeline = models.TextField()
    contact_id = models.TextField(blank=True, null=True)
    name = models.TextField()
    stage = models.TextField()
    amount = models.FloatField(blank=True, null=True)
    probability = models.FloatField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    last_contact_at = models.DateTimeField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_date = models.TextField(blank=True, null=True)
    stale_days = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    wire_transaction_id = models.TextField(blank=True, null=True)
    commitment_date = models.TextField(blank=True, null=True)
    wire_date = models.TextField(blank=True, null=True)
    docs_status = models.TextField(blank=True, null=True)
    investor_email = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "pipeline_deals"


class SenderReputation(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    sender = models.TextField()
    source = models.TextField()
    classification = models.TextField()
    confidence = models.FloatField(blank=True, null=True)
    total_messages = models.IntegerField(blank=True, null=True)
    routed_count = models.IntegerField(blank=True, null=True)
    filed_count = models.IntegerField(blank=True, null=True)
    dismissed_count = models.IntegerField(blank=True, null=True)
    user_overrides = models.IntegerField(blank=True, null=True)
    last_message_at = models.DateTimeField(blank=True, null=True)
    last_classification = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "sender_reputation"
        unique_together = (("sender", "tenant_id"),)


class SlackMessages(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    channel = models.TextField()
    sender = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    highlight = models.IntegerField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    triage_status = models.TextField(blank=True, null=True)
    triage_classification = models.TextField(blank=True, null=True)
    triage_run_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "slack_messages"
