# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models


class PricingAddons(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    price_cents = models.IntegerField()
    billing_type = models.TextField()
    billing_interval = models.TextField(blank=True, null=True)
    tier_requirement = models.TextField(blank=True, null=True)
    stripe_price_id = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "pricing_addons"
