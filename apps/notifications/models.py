# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class FeatureAnnouncements(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    feature_key = models.TextField()
    title = models.TextField()
    body = models.TextField()
    relevant_roles = models.TextField(blank=True, null=True)
    action_label = models.TextField(blank=True, null=True)
    action_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "feature_announcements"


class HubNotifications(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    user_email = models.TextField()
    type = models.TextField()
    title = models.TextField()
    body = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    source_agent_id = models.TextField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "hub_notifications"


class Notifications(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    type = models.TextField()
    title = models.TextField()
    body = models.TextField(blank=True, null=True)
    action_url = models.TextField(blank=True, null=True)
    is_read = models.IntegerField()
    entity_id = models.TextField(blank=True, null=True)
    source = models.TextField()
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "notifications"


class PageTips(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    user_email = models.TextField()
    page_id = models.TextField()
    tip_text = models.TextField()
    capabilities_json = models.JSONField(blank=True, null=True)
    dismissed = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "page_tips"
        unique_together = (("user_email", "page_id"),)


class TourGuideProgress(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    user_email = models.TextField()
    step_type = models.TextField()
    step_id = models.TextField()
    status = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    dismissed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "tour_guide_progress"
        unique_together = (("user_email", "step_id"),)
