# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class AgentArtifacts(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    user_email = models.TextField()
    title = models.TextField()
    artifact_type = models.TextField()
    content_html = models.TextField(blank=True, null=True)
    content_markdown = models.TextField(blank=True, null=True)
    template = models.TextField(blank=True, null=True)
    file_url = models.TextField(blank=True, null=True)
    run_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    brief_type = models.TextField(blank=True, null=True)
    assigned_to = models.TextField(blank=True, null=True)
    assigned_by = models.TextField(blank=True, null=True)
    presenting_agent_id = models.TextField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    shared_thread_id = models.TextField(blank=True, null=True)
    published_url = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    publish_target = models.TextField(blank=True, null=True)
    publish_slug = models.TextField(blank=True, null=True)
    publish_status = models.TextField(blank=True, null=True)
    media_type = models.TextField(blank=True, null=True)
    source_file = models.TextField(blank=True, null=True)
    contact_id = models.TextField(blank=True, null=True)
    company_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "agent_artifacts"


class AskActions(models.Model):
    id = models.TextField(primary_key=True)
    conversation_id = models.TextField(blank=True, null=True)
    message_id = models.TextField(blank=True, null=True)
    action_type = models.TextField()
    action_params_json = models.JSONField(blank=True, null=True)
    status = models.TextField()
    confirmed_by = models.TextField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    executed_at = models.DateTimeField(blank=True, null=True)
    result_json = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "ask_actions"


class AskConversations(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    agents_json = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "ask_conversations"


class AskMessages(models.Model):
    id = models.TextField(primary_key=True)
    conversation = models.ForeignKey(AskConversations, models.DO_NOTHING)
    role = models.TextField()
    content = models.TextField()
    sources_json = models.JSONField(blank=True, null=True)
    agent = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    confidence = models.TextField(blank=True, null=True)
    follow_ups_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "ask_messages"


class AskResponses(models.Model):
    id = models.TextField(primary_key=True)
    ask_id = models.TextField()
    investor_profile_id = models.TextField()
    investor_name = models.TextField()
    body = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "ask_responses"


class Asks(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    target_investor_ids = models.TextField(blank=True, null=True)
    status = models.TextField()
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "asks"


class BriefActions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    source_type = models.TextField()
    source_id = models.TextField()
    action_type = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    assigned_to = models.TextField(blank=True, null=True)
    due_date = models.TextField(blank=True, null=True)
    calendar_event_id = models.TextField(blank=True, null=True)
    task_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "brief_actions"


class BriefCache(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    tenant_id = models.TextField(blank=True, null=True)
    sections_json = models.JSONField()
    strip_json = models.JSONField(blank=True, null=True)
    generated_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "brief_cache"
        unique_together = (("user_email", "tenant_id"),)


class BriefCards(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    agent_id = models.TextField()
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    zone = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    action_label = models.TextField(blank=True, null=True)
    action_type = models.TextField(blank=True, null=True)
    action_payload = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "brief_cards"


class BriefDeliveries(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.ForeignKey(
        "hub_auth.People", models.DO_NOTHING, db_column="user_email", to_field="email"
    )
    type = models.TextField()
    status = models.TextField()
    error = models.TextField(blank=True, null=True)
    resend_id = models.TextField(blank=True, null=True)
    delivered_at = models.DateTimeField()

    class Meta:
        db_table = "brief_deliveries"


class BriefPins(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.TextField()
    item_type = models.TextField()
    user_email = models.TextField()
    title = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "brief_pins"
        unique_together = (("item_id", "user_email"),)


class BriefPreferences(models.Model):
    email = models.TextField(primary_key=True)
    daily_enabled = models.IntegerField()
    weekly_enabled = models.IntegerField()
    delivery_time = models.TextField()
    timezone = models.TextField()
    format = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "brief_preferences"


class EmailTemplates(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    subject_template = models.TextField()
    body_template = models.TextField()
    category = models.TextField()
    entity_id = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    variables_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "email_templates"
