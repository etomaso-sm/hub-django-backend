# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class AgentKpis(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    agent_id = models.TextField()
    period = models.TextField()
    total_runs = models.IntegerField(blank=True, null=True)
    successful_runs = models.IntegerField(blank=True, null=True)
    approval_rate = models.FloatField(blank=True, null=True)
    avg_response_time_ms = models.IntegerField(blank=True, null=True)
    user_edits = models.IntegerField(blank=True, null=True)
    rejections = models.IntegerField(blank=True, null=True)
    escalations = models.IntegerField(blank=True, null=True)
    hallucination_flags = models.IntegerField(blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)
    cost_usd = models.FloatField(blank=True, null=True)
    autonomy_level_avg = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "agent_kpis"
        unique_together = (("agent_id", "period"),)


class ClientHealthScores(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    client_id = models.TextField()
    client_name = models.TextField(blank=True, null=True)
    health_score = models.IntegerField(blank=True, null=True)
    churn_risk = models.IntegerField(blank=True, null=True)
    revenue_monthly = models.FloatField(blank=True, null=True)
    revenue_trend = models.TextField(blank=True, null=True)
    ar_aging_days = models.IntegerField(blank=True, null=True)
    last_comm_days = models.IntegerField(blank=True, null=True)
    jockey_conversion_ready = models.IntegerField(blank=True, null=True)
    jockey_margin_estimate = models.FloatField(blank=True, null=True)
    signals = models.JSONField(blank=True, null=True)
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "client_health_scores"


class PageAnalytics(models.Model):
    id = models.TextField(primary_key=True)
    viewer_name = models.TextField(blank=True, null=True)
    viewer_email = models.TextField(blank=True, null=True)
    event = models.TextField()
    page = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    referrer = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_country = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    internal = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "page_analytics"


class TeamAnalytics(models.Model):
    id = models.TextField(primary_key=True)
    user_email = models.TextField()
    period = models.TextField()
    automation_pct = models.FloatField(blank=True, null=True)
    hub_sessions = models.IntegerField(blank=True, null=True)
    hub_minutes = models.FloatField(blank=True, null=True)
    slack_messages = models.IntegerField(blank=True, null=True)
    gmail_sent = models.IntegerField(blank=True, null=True)
    gmail_received = models.IntegerField(blank=True, null=True)
    jira_updates = models.IntegerField(blank=True, null=True)
    deel_hours = models.FloatField(blank=True, null=True)
    top_agents = models.TextField(blank=True, null=True)
    focus_areas = models.TextField(blank=True, null=True)
    struggle_signals = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "team_analytics"
        unique_together = (("user_email", "period"),)
