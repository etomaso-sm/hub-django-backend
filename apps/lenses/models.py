# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ContentApprovals(models.Model):
    id = models.TextField(primary_key=True)
    content_item_id = models.TextField()
    approver_user_id = models.TextField()
    approver_name = models.TextField()
    action = models.TextField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "content_approvals"


class ContentItems(models.Model):
    id = models.TextField(primary_key=True)
    ir_calendar_item_id = models.TextField(blank=True, null=True)
    type = models.TextField()
    title = models.TextField()
    body = models.TextField(blank=True, null=True)
    body_html = models.TextField(blank=True, null=True)
    status = models.TextField()
    author_user_id = models.TextField(blank=True, null=True)
    author_name = models.TextField(blank=True, null=True)
    required_approvals = models.IntegerField()
    current_approvals = models.IntegerField()
    scheduled_for = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "content_items"


class ContentLibrary(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    content_type = models.TextField()
    body = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    target_audience = models.TextField(blank=True, null=True)
    channel = models.TextField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "content_library"


class DeckTemplates(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    deck_type = models.TextField()
    slide_structure = models.JSONField()
    data_sources = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "deck_templates"


class IrCalendarItems(models.Model):
    id = models.TextField(primary_key=True)
    category = models.TextField()
    type = models.TextField()
    title = models.TextField()
    period = models.TextField(blank=True, null=True)
    due_date = models.TextField(blank=True, null=True)
    review_by = models.TextField(blank=True, null=True)
    status = models.TextField()
    owner_user_id = models.TextField(blank=True, null=True)
    owner_name = models.TextField(blank=True, null=True)
    ai_suggested = models.IntegerField()
    trigger_description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    scheduled_for = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    content_item_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "ir_calendar_items"


class IrCommunications(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField()
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    audience = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "ir_communications"


class NarrativeContexts(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    entity = models.TextField()
    status = models.TextField(blank=True, null=True)
    positioning = models.TextField(blank=True, null=True)
    key_facts = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "narrative_contexts"


class NarrativeFaqs(models.Model):
    id = models.TextField(primary_key=True)
    entity = models.TextField()
    audience = models.TextField()
    question = models.TextField()
    answer = models.TextField()
    source = models.TextField(blank=True, null=True)
    verified = models.IntegerField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    pushed_to_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "narrative_faqs"


class NarrativePushes(models.Model):
    id = models.TextField(primary_key=True)
    narrative_version_id = models.TextField()
    target_agent = models.TextField()
    pushed_at = models.DateTimeField(blank=True, null=True)
    acknowledged = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "narrative_pushes"


class NarrativeSignals(models.Model):
    id = models.TextField(primary_key=True)
    source_agent = models.TextField()
    signal_type = models.TextField()
    entity = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    processed = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    data_json = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "narrative_signals"


class NarrativeThreads(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    title = models.TextField()
    entity = models.TextField(blank=True, null=True)
    audience = models.TextField(blank=True, null=True)
    messages_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "narrative_threads"


class NarrativeVersions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    variant = models.TextField()
    audience = models.TextField()
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    doc_type = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    stale_reason = models.TextField(blank=True, null=True)
    last_verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "narrative_versions"
