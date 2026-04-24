# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ClientInvoices(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    client_id = models.TextField()
    number = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    status = models.TextField()
    date = models.TextField(blank=True, null=True)
    due_date = models.TextField(blank=True, null=True)
    paid_date = models.TextField(blank=True, null=True)
    qb_invoice_id = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    stripe_invoice_id = models.TextField(blank=True, null=True)
    stripe_customer_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "client_invoices"


class ClientMessages(models.Model):
    id = models.TextField(primary_key=True)
    client_id = models.TextField()
    sender_email = models.TextField()
    sender_name = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField()
    is_internal = models.IntegerField()

    class Meta:
        db_table = "client_messages"


class ClientUsers(models.Model):
    id = models.TextField(primary_key=True)
    email = models.TextField(unique=True)
    client_id = models.TextField()
    name = models.TextField()
    role = models.TextField(blank=True, null=True)
    status = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "client_users"


class HubSubscriptions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(unique=True)
    plan = models.TextField()
    stripe_customer_id = models.TextField(blank=True, null=True)
    stripe_subscription_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    mrr_cents = models.IntegerField(blank=True, null=True)
    trial_ends_at = models.DateTimeField(blank=True, null=True)
    billing_email = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    billing_cycle = models.TextField(blank=True, null=True)
    current_period_end = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "hub_subscriptions"


class SaasSubscriptions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    tool_name = models.TextField()
    vendor = models.TextField(blank=True, null=True)
    monthly_cost = models.FloatField(blank=True, null=True)
    annual_cost = models.FloatField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    hub_replacement_agent = models.TextField(blank=True, null=True)
    replacement_status = models.TextField(blank=True, null=True)
    replacement_notes = models.TextField(blank=True, null=True)
    dependencies_json = models.JSONField(blank=True, null=True)
    data_migrated = models.IntegerField(blank=True, null=True)
    cancel_date = models.TextField(blank=True, null=True)
    savings_to_date = models.FloatField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "saas_subscriptions"


class SubscriptionAddons(models.Model):
    objects = TenantScopedManager()
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.TextField()
    addon = models.ForeignKey("pricing.PricingAddons", models.DO_NOTHING)
    status = models.TextField()
    quantity = models.IntegerField()
    stripe_subscription_item_id = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "subscription_addons"
        unique_together = (("tenant_id", "addon"),)


class SubscriptionChanges(models.Model):
    objects = TenantScopedManager()
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.TextField()
    change_type = models.TextField()
    old_plan = models.TextField(blank=True, null=True)
    new_plan = models.TextField(blank=True, null=True)
    addon_id = models.TextField(blank=True, null=True)
    stripe_event_id = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "subscription_changes"


class TenantInvites(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    email = models.TextField()
    role = models.TextField(blank=True, null=True)
    invited_by = models.TextField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "tenant_invites"
        unique_together = (("tenant_id", "email"),)
