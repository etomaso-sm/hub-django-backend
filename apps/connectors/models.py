# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ConnectorConfigs(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    provider = models.TextField(unique=True)
    status = models.TextField()
    connected_by = models.TextField(blank=True, null=True)
    connected_at = models.DateTimeField(blank=True, null=True)
    last_sync = models.TextField(blank=True, null=True)
    sync_frequency = models.IntegerField(blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sync_count = models.IntegerField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "connector_configs"


class ConnectorRegistry(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    provider = models.TextField()
    connector_type = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    data_scope = models.TextField(blank=True, null=True)
    health_score = models.FloatField(blank=True, null=True)
    last_sync = models.TextField(blank=True, null=True)
    lifecycle_stage = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "connector_registry"


class ConnectorSyncLog(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    provider = models.TextField()
    status = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "connector_sync_log"


class Connectors(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    provider = models.TextField()
    status = models.TextField()
    last_sync = models.TextField(blank=True, null=True)
    config_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "connectors"


class HubExternalData(models.Model):
    id = models.TextField(primary_key=True)
    source_hub_url = models.TextField()
    source_hub_name = models.TextField(blank=True, null=True)
    field = models.TextField()
    value = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "hub_external_data"


class PrivacyBrokers(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    domain = models.TextField()
    opt_out_url = models.TextField(blank=True, null=True)
    scan_enabled = models.IntegerField(blank=True, null=True)
    removal_enabled = models.IntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    difficulty = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "privacy_brokers"


class PrivacyRemovals(models.Model):
    id = models.TextField(primary_key=True)
    subscriber_id = models.TextField()
    scan_id = models.TextField(blank=True, null=True)
    broker_name = models.TextField()
    broker_url = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "privacy_removals"


class PrivacyScans(models.Model):
    id = models.TextField(primary_key=True)
    subscriber_id = models.TextField()
    status = models.TextField(blank=True, null=True)
    scan_type = models.TextField(blank=True, null=True)
    brokers_checked = models.IntegerField(blank=True, null=True)
    brokers_found = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    results_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "privacy_scans"


class PrivacySubscribers(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    email = models.TextField()
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)
    stripe_customer_id = models.TextField(blank=True, null=True)
    stripe_subscription_id = models.TextField(blank=True, null=True)
    pii_json = models.JSONField(blank=True, null=True)
    scan_status = models.TextField(blank=True, null=True)
    last_scan_at = models.DateTimeField(blank=True, null=True)
    broker_count = models.IntegerField(blank=True, null=True)
    removed_count = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "privacy_subscribers"


class SyncLog(models.Model):
    id = models.TextField(primary_key=True)
    connector = models.ForeignKey(ConnectorConfigs, models.DO_NOTHING)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.TextField()
    records_synced = models.IntegerField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "sync_log"
