# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ReconciliationLog(models.Model):
    id = models.TextField(primary_key=True)
    period = models.TextField()
    bank_balance = models.FloatField(blank=True, null=True)
    qb_balance = models.FloatField(blank=True, null=True)
    hub_balance = models.FloatField(blank=True, null=True)
    discrepancy = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "reconciliation_log"


class ReconciliationTasks(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    period = models.TextField()
    task_type = models.TextField()
    description = models.TextField()
    bank_txn_id = models.TextField(blank=True, null=True)
    qb_txn_id = models.TextField(blank=True, null=True)
    hub_txn_id = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    suggested_action = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    resolved_by = models.TextField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    assigned_to = models.TextField(blank=True, null=True)
    escalated_by = models.TextField(blank=True, null=True)
    escalated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "reconciliation_tasks"
