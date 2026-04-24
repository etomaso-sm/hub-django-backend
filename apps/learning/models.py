# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class BlendedClones(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    clone_weights = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "blended_clones"


class CloneDecisions(models.Model):
    id = models.TextField(primary_key=True)
    clone_id = models.TextField(blank=True, null=True)
    scenario_id = models.TextField(blank=True, null=True)
    clone_decision = models.TextField(blank=True, null=True)
    human_decision = models.TextField(blank=True, null=True)
    agreement = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clone_decisions"


class CloneProfiles(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    user_email = models.TextField()
    clone_name = models.TextField(blank=True, null=True)
    operating_manual = models.TextField(blank=True, null=True)
    decision_frameworks = models.TextField(blank=True, null=True)
    communication_style = models.TextField(blank=True, null=True)
    priorities = models.TextField(blank=True, null=True)
    quality_bar = models.TextField(blank=True, null=True)
    blind_spots = models.TextField(blank=True, null=True)
    strengths = models.TextField(blank=True, null=True)
    common_phrases = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    training_progress = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clone_profiles"


class CloneScenarios(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    expected_decision = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clone_scenarios"


class CloneTrainingSignals(models.Model):
    id = models.TextField(primary_key=True)
    clone_id = models.TextField(blank=True, null=True)
    signal_type = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    decision_made = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "clone_training_signals"


class TrainingNeeds(models.Model):
    id = models.TextField(primary_key=True)
    person_email = models.TextField()
    skill_name = models.TextField()
    current_level = models.TextField(blank=True, null=True)
    target_level = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "training_needs"


class UserPatterns(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    tenant_id = models.TextField()
    user_email = models.TextField()
    pattern_type = models.TextField()
    pattern = models.TextField()
    confidence = models.FloatField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user_patterns"
