# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class VaultAccessLog(models.Model):
    id = models.TextField(primary_key=True)
    vault_item_id = models.TextField()
    accessed_by = models.TextField()
    action = models.TextField()
    ip_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "vault_access_log"


class VaultAuthTokens(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    token = models.TextField(unique=True)
    expires_at = models.DateTimeField()
    used = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "vault_auth_tokens"


class VaultItems(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    owner = models.TextField()
    category = models.TextField()
    label = models.TextField()
    has_secondary = models.IntegerField(blank=True, null=True)
    secondary_label = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    renewal_url = models.TextField(blank=True, null=True)
    renewal_lead_days = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    last_accessed_at = models.DateTimeField(blank=True, null=True)
    access_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    shared = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "vault_items"


class WebauthnCredentials(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    credential_id = models.TextField(unique=True)
    public_key = models.TextField()
    sign_count = models.IntegerField(blank=True, null=True)
    transports = models.TextField(blank=True, null=True)
    device_name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "webauthn_credentials"
