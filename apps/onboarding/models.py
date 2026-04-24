# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class OnboardingSavings(models.Model):
    objects = TenantScopedManager()
    id = models.BigAutoField(primary_key=True)
    tenant_id = models.TextField()
    tool_name = models.TextField()
    category = models.TextField()
    reported_cost_cents = models.IntegerField()
    hub_replacement = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "onboarding_savings"


class OnboardingSessions(models.Model):
    id = models.TextField(primary_key=True)
    company_id = models.TextField(blank=True, null=True)
    step = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "onboarding_sessions"
