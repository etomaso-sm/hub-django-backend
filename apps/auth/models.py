# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class People(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    email = models.TextField(unique=True)
    display_name = models.TextField()
    role = models.TextField()
    tier = models.TextField()
    title = models.TextField(blank=True, null=True)
    division = models.TextField(blank=True, null=True)
    entity_access = models.JSONField()
    scopes = models.JSONField()
    agents = models.JSONField()
    default_agent = models.TextField(blank=True, null=True)
    status = models.TextField()
    avatar_url = models.TextField(blank=True, null=True)
    monitoring_tier = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    photo_url = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    is_workspace_admin = models.IntegerField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "people"

    @property
    def is_authenticated(self) -> bool:
        return True


class UserIdentityLinks(models.Model):
    id = models.TextField(primary_key=True)
    user_id = models.TextField()
    email = models.TextField(unique=True)
    email_type = models.TextField(blank=True, null=True)
    is_primary = models.IntegerField(blank=True, null=True)
    verified = models.IntegerField(blank=True, null=True)
    linked_at = models.DateTimeField(blank=True, null=True)
    linked_by = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_identity_links"


class UserTenants(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    tenant_id = models.TextField()
    role = models.TextField(blank=True, null=True)
    is_owner = models.IntegerField(blank=True, null=True)
    is_admin = models.IntegerField(blank=True, null=True)
    joined_at = models.DateTimeField()
    access_tier = models.IntegerField(blank=True, null=True)
    ui_mode = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_tenants"
        unique_together = (("user_email", "tenant_id"),)
