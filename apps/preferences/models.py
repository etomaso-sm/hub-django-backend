# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class CustomSidebarSections(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    agent_id = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    section_schema = models.TextField(blank=True, null=True)
    data_sources = models.JSONField(blank=True, null=True)
    created_by = models.TextField()
    proposal_id = models.TextField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "custom_sidebar_sections"


class FeatureAnnouncementViews(models.Model):
    id = models.TextField(primary_key=True)
    announcement_id = models.TextField()
    user_email = models.TextField()
    shown_at = models.DateTimeField(blank=True, null=True)
    dismissed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "feature_announcement_views"
        unique_together = (("announcement_id", "user_email"),)


class NotificationPreferences(models.Model):
    # Composite primary key (email, type) is not supported; inspectdb selected email.
    email = models.TextField(primary_key=True)
    type = models.TextField()
    in_app = models.IntegerField()
    push_email = models.IntegerField()
    sound = models.IntegerField()

    class Meta:
        db_table = "notification_preferences"
        unique_together = (("email", "type"),)


class RoleTemplates(models.Model):
    id = models.TextField(primary_key=True)
    role_name = models.TextField()
    description = models.TextField(blank=True, null=True)
    agent_permissions = models.TextField()
    sidebar_default = models.TextField(blank=True, null=True)
    brief_agents = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "role_templates"


class SharingConfig(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    target_hub_url = models.TextField()
    target_hub_name = models.TextField(blank=True, null=True)
    fields_shared = models.TextField(blank=True, null=True)
    secret = models.TextField(blank=True, null=True)
    granted_by = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "sharing_config"


class SidebarSectionShares(models.Model):
    id = models.TextField(primary_key=True)
    section_id = models.TextField()
    shared_by = models.TextField()
    shared_with = models.TextField()
    status = models.TextField(blank=True, null=True)
    shared_at = models.DateTimeField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "sidebar_section_shares"


class UserAgentPermissions(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    agent_id = models.TextField()
    can_view = models.IntegerField(blank=True, null=True)
    can_chat = models.IntegerField(blank=True, null=True)
    can_approve = models.IntegerField(blank=True, null=True)
    can_see_financials = models.IntegerField(blank=True, null=True)
    can_configure = models.IntegerField(blank=True, null=True)
    can_execute = models.IntegerField(blank=True, null=True)
    set_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    tone = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_agent_permissions"
        unique_together = (("user_email", "agent_id"),)


class UserFeatureUsage(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    user_email = models.TextField()
    feature_key = models.TextField()
    first_used_at = models.DateTimeField(blank=True, null=True)
    use_count = models.IntegerField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user_feature_usage"
        unique_together = (("user_email", "feature_key"),)


class UserPreferences(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField(unique=True)
    default_view = models.TextField(blank=True, null=True)
    sidebar_order_json = models.JSONField(blank=True, null=True)
    brief_emphasis_json = models.JSONField(blank=True, null=True)
    notification_filters_json = models.JSONField(blank=True, null=True)
    dashboard_layout_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    agent_domains = models.JSONField(blank=True, null=True)
    pinned_items = models.JSONField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    vault_pin = models.TextField(blank=True, null=True)
    onboarding_completed = models.IntegerField()
    display_settings = models.JSONField(blank=True, null=True)
    agent_sort_pref = models.TextField(blank=True, null=True)
    pinned_agents = models.JSONField(blank=True, null=True)
    hide_inactive_agents = models.IntegerField(blank=True, null=True)
    team_tour_completed = models.IntegerField(blank=True, null=True)
    team_tour_data = models.JSONField(blank=True, null=True)
    last_brief_generated = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_preferences"
