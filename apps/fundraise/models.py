# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class CapTableEntries(models.Model):
    id = models.TextField(primary_key=True)
    investor_profile_id = models.TextField(blank=True, null=True)
    name = models.TextField()
    type = models.TextField()
    class_field = models.TextField(
        db_column="class"
    )  # Field renamed because it was a Python reserved word.
    units = models.IntegerField()
    invested_amount = models.IntegerField()
    post_pref_pct = models.FloatField()
    post_eip_pct = models.FloatField()
    voting_pct = models.FloatField()
    vesting = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    portal_visible = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "cap_table_entries"


class FundDocuments(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    category = models.TextField()
    description = models.TextField(blank=True, null=True)
    doc_url = models.TextField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    visibility = models.TextField()
    published_date = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "fund_documents"


class FundMetrics(models.Model):
    id = models.TextField(primary_key=True)
    period = models.TextField()
    fund_size = models.FloatField()
    committed = models.FloatField()
    deployed = models.FloatField()
    distributions = models.FloatField()
    irr = models.FloatField(blank=True, null=True)
    tvpi = models.FloatField(blank=True, null=True)
    dpi = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "fund_metrics"


class FundraiseCampaignProspects(models.Model):
    id = models.TextField(primary_key=True)
    campaign_id = models.TextField()
    investor_id = models.TextField()
    sequence_id = models.TextField(blank=True, null=True)
    page_token = models.TextField(blank=True, null=True)
    page_artifact_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "fundraise_campaign_prospects"


class FundraiseCampaigns(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    name = models.TextField()
    raise_id = models.TextField(blank=True, null=True)
    icp_description = models.TextField(blank=True, null=True)
    instrument = models.TextField(blank=True, null=True)
    valuation_cap = models.FloatField(blank=True, null=True)
    min_check = models.FloatField(blank=True, null=True)
    cadence_template_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    stats_json = models.JSONField(blank=True, null=True)
    playbook_json = models.JSONField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "fundraise_campaigns"


class FundraiseTracking(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    entity_id = models.TextField()
    raise_name = models.TextField()
    target_amount = models.FloatField()
    committed_amount = models.FloatField()
    owner = models.TextField()
    status = models.TextField()
    stage = models.TextField()
    vehicle = models.TextField(blank=True, null=True)
    deadline = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "fundraise_tracking"


class IcMeetings(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    date = models.TextField()
    attendees = models.TextField(blank=True, null=True)
    agenda = models.TextField(blank=True, null=True)
    minutes = models.TextField(blank=True, null=True)
    deals_reviewed = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "ic_meetings"


class IcVotes(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    deal_id = models.TextField()
    voter_email = models.TextField()
    vote = models.TextField()
    rationale = models.TextField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "ic_votes"


class InvestorEngagementLog(models.Model):
    id = models.TextField(primary_key=True)
    investor_id = models.TextField()
    viewer_email = models.TextField()
    page = models.TextField(blank=True, null=True)
    event = models.TextField()
    notified_to = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "investor_engagement_log"


class InvestorProfiles(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    entity_name = models.TextField(blank=True, null=True)
    amount_committed = models.IntegerField(blank=True, null=True)
    amount_funded = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    tranche = models.IntegerField(blank=True, null=True)
    docs_signed = models.IntegerField(blank=True, null=True)
    date_funded = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    share_token = models.TextField(blank=True, null=True)
    last_view_at = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "investor_profiles"


class InvestorTransactions(models.Model):
    id = models.TextField(primary_key=True)
    investor_id = models.TextField()
    type = models.TextField()
    amount = models.FloatField()
    date = models.TextField()
    status = models.TextField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "investor_transactions"


class InvestorUpdates(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    date = models.TextField()
    visibility = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "investor_updates"


class InvestorUsers(models.Model):
    id = models.TextField(primary_key=True)
    email = models.TextField(unique=True)
    investor_id = models.TextField()
    name = models.TextField()
    status = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "investor_users"


class ProspectDecisions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    investor_id = models.TextField()
    campaign_id = models.TextField(blank=True, null=True)
    decision = models.TextField()
    reason = models.TextField(blank=True, null=True)
    decided_by = models.TextField()
    attributes_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "prospect_decisions"
