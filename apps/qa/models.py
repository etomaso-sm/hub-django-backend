# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class ElleAgentScores(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    total_journeys = models.IntegerField(blank=True, null=True)
    passed_journeys = models.IntegerField(blank=True, null=True)
    failed_journeys = models.IntegerField(blank=True, null=True)
    consecutive_passes = models.IntegerField(blank=True, null=True)
    consecutive_fails = models.IntegerField(blank=True, null=True)
    correction_rate_50 = models.FloatField(blank=True, null=True)
    correction_rate_200 = models.FloatField(blank=True, null=True)
    correction_rate_1000 = models.FloatField(blank=True, null=True)
    last_run_id = models.TextField(blank=True, null=True)
    last_run_status = models.TextField(blank=True, null=True)
    last_run_at = models.DateTimeField(blank=True, null=True)
    recommended_level = models.IntegerField(blank=True, null=True)
    current_level = models.IntegerField(blank=True, null=True)
    security_violations = models.IntegerField(blank=True, null=True)
    last_demotion_at = models.DateTimeField(blank=True, null=True)
    last_promotion_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "elle_agent_scores"
        unique_together = (("agent_id", "tenant_id"),)


class ElleAssertions(models.Model):
    id = models.TextField(primary_key=True)
    run = models.ForeignKey("ElleRuns", models.DO_NOTHING)
    step_index = models.IntegerField()
    step_name = models.TextField(blank=True, null=True)
    assertion_type = models.TextField()
    expected = models.TextField(blank=True, null=True)
    actual = models.TextField(blank=True, null=True)
    passed = models.IntegerField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    duration_ms = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "elle_assertions"


class ElleJourneys(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    agent_id = models.TextField()
    trigger_type = models.TextField()
    trigger_filter = models.TextField(blank=True, null=True)
    steps_json = models.JSONField()
    active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "elle_journeys"


class ElleRuns(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    journey = models.ForeignKey(ElleJourneys, models.DO_NOTHING)
    status = models.TextField()
    total_steps = models.IntegerField(blank=True, null=True)
    passed_steps = models.IntegerField(blank=True, null=True)
    failed_steps = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    results_json = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    duration_ms = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "elle_runs"
