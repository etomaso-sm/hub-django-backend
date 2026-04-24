# mypy: disable-error-code=misc
"""Django model declarations generated from TKT-019 inspectdb output."""

from django.db import models

from apps.common.managers import TenantScopedManager


class BankTransactions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    plaid_transaction_id = models.TextField(blank=True, null=True)
    account_id = models.TextField(blank=True, null=True)
    date = models.TextField()
    amount = models.FloatField()
    name = models.TextField(blank=True, null=True)
    merchant_name = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    hub_category = models.TextField(blank=True, null=True)
    hub_category_confidence = models.FloatField(blank=True, null=True)
    pending = models.IntegerField(blank=True, null=True)
    matched_qb_txn_id = models.TextField(blank=True, null=True)
    matched_hub_txn_id = models.TextField(blank=True, null=True)
    match_confidence = models.FloatField(blank=True, null=True)
    match_method = models.TextField(blank=True, null=True)
    reviewed_by = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    raw_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "bank_transactions"


class ChartOfAccounts(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    account_number = models.TextField(unique=True)
    account_name = models.TextField()
    account_type = models.TextField()
    hub_category = models.TextField(blank=True, null=True)
    parent_account_id = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "chart_of_accounts"


class DeelContractors(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    contract_type = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    monthly_amount = models.FloatField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    end_date = models.TextField(blank=True, null=True)
    job_title = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "deel_contractors"


class DeelInvoices(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    contractor_id = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    period_start = models.TextField(blank=True, null=True)
    period_end = models.TextField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "deel_invoices"


class DeelPayments(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    contractor_id = models.TextField(blank=True, null=True)
    contract_id = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    payment_type = models.TextField(blank=True, null=True)
    period_start = models.TextField(blank=True, null=True)
    period_end = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.TextField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    deel_payment_id = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "deel_payments"


class ExpenseBreakdown(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    period = models.TextField()
    category = models.TextField()
    vendor = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    replaceable_by_hub = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "expense_breakdown"


class FinanceSnapshots(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    entity = models.ForeignKey("hub_app.Entities", models.DO_NOTHING)
    period = models.TextField()
    cash_position = models.FloatField(blank=True, null=True)
    revenue_monthly = models.FloatField(blank=True, null=True)
    burn_monthly = models.FloatField(blank=True, null=True)
    runway_months = models.FloatField(blank=True, null=True)
    ar_outstanding = models.FloatField(blank=True, null=True)
    ap_outstanding = models.FloatField(blank=True, null=True)
    headcount = models.IntegerField(blank=True, null=True)
    rev_per_employee = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "finance_snapshots"


class FinancialScenarios(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    assumptions = models.JSONField()
    results = models.JSONField()
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "financial_scenarios"


class MonthlyClose(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    period = models.TextField()
    step_name = models.TextField()
    status = models.TextField(blank=True, null=True)
    completed_by = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "monthly_close"


class QbTransactions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    connector_id = models.TextField()
    txn_id = models.TextField(unique=True)
    type = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    account = models.TextField(blank=True, null=True)
    entity_id = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    raw_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField()
    tenant_id = models.TextField(blank=True, null=True)
    hub_category_confidence = models.FloatField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "qb_transactions"


class RampTransactions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    ramp_id = models.TextField(unique=True, blank=True, null=True)
    date = models.TextField()
    amount = models.FloatField()
    merchant_name = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    card_name = models.TextField(blank=True, null=True)
    raw_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    hub_category = models.TextField(blank=True, null=True)
    hub_category_confidence = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "ramp_transactions"


class SmTools(models.Model):
    id = models.TextField(primary_key=True)
    vendor = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    monthly_cost = models.FloatField(blank=True, null=True)
    hub_replaces = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "sm_tools"


class StripeTransactions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    charge_id = models.TextField(unique=True, blank=True, null=True)
    date = models.TextField()
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    customer_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    matched_invoice_id = models.TextField(blank=True, null=True)
    raw_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "stripe_transactions"


class ToolInventory(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    monthly_cost = models.FloatField(blank=True, null=True)
    owner_email = models.TextField(blank=True, null=True)
    division = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    hub_replacement = models.TextField(blank=True, null=True)
    has_api = models.IntegerField(blank=True, null=True)
    api_connected = models.IntegerField(blank=True, null=True)
    connection_status = models.TextField(blank=True, null=True)
    last_charge_date = models.TextField(blank=True, null=True)
    charge_count = models.IntegerField(blank=True, null=True)
    total_spend = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    decision = models.TextField(blank=True, null=True)
    decided_by = models.TextField(blank=True, null=True)
    decided_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)
    replacement_status = models.TextField(blank=True, null=True)
    replacement_notes = models.TextField(blank=True, null=True)
    dependencies_json = models.JSONField(blank=True, null=True)
    savings_to_date = models.FloatField(blank=True, null=True)
    cancel_date = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    hub_replacement_agent = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    hours_automated = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "tool_inventory"


class Transactions(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    date = models.TextField()
    description = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    type = models.TextField()
    category = models.TextField(blank=True, null=True)
    category_confidence = models.FloatField(blank=True, null=True)
    categorized_by = models.TextField(blank=True, null=True)
    reconciled = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    account_number = models.TextField(blank=True, null=True)
    bank_txn_id = models.TextField(blank=True, null=True)
    qb_txn_id = models.TextField(blank=True, null=True)
    match_confidence = models.FloatField(blank=True, null=True)
    match_method = models.TextField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "transactions"


class VendorRules(models.Model):
    objects = TenantScopedManager()
    id = models.TextField(primary_key=True)
    vendor_pattern = models.TextField(unique=True)
    hub_category = models.TextField()
    account_number = models.TextField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    created_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tenant_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "vendor_rules"
