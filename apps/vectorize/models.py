# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class HubKnowledge(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    filename = models.TextField()
    content = models.TextField()
    category = models.TextField()
    updated_at = models.DateTimeField()
    section_slug = models.TextField(blank=True, null=True)
    assigned_to = models.TextField(blank=True, null=True)
    entry_type = models.TextField(blank=True, null=True)
    searchable_keywords = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    access_tier = models.IntegerField(blank=True, null=True)
    knowledge_domain = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "hub_knowledge"
