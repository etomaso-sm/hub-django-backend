"""System checks that enforce the tenant-scoping discipline.

Registered by ``apps.common.apps.CommonConfig.ready()``. The check walks the
Django app registry and fails startup if any managed model with a
``tenant_id`` field does not use ``TenantScopedManager`` (or a subclass).

Rationale: tenant isolation is a load-bearing invariant for this codebase. A
missed filter is a silent cross-tenant leak. Enforcing at startup time means
any new model with `tenant_id` is caught before it ships.
"""

from collections.abc import Iterable
from typing import Any

from django.apps import apps
from django.core.checks import CheckMessage, Error, register


@register()  # type: ignore[untyped-decorator]  # django.core.checks.register is untyped
def check_tenant_managers(app_configs: Any, **kwargs: Any) -> Iterable[CheckMessage]:
    # Imported lazily so this module stays importable before Django has fully
    # loaded (the check is registered at AppConfig.ready time, but we also
    # want to avoid circular-import surprises via `apps.common.managers`).
    from apps.common.managers import TenantScopedManager

    errors: list[CheckMessage] = []
    for model in apps.get_models():
        if not model._meta.managed:
            continue
        if not _has_tenant_id_field(model):
            continue
        if not isinstance(model._default_manager, TenantScopedManager):
            errors.append(
                Error(
                    f"{model._meta.label} has a `tenant_id` field but its default "
                    "manager is not TenantScopedManager. Cross-tenant reads are "
                    "possible. Set `objects = TenantScopedManager()` on the model, "
                    "or use an explicit subclass.",
                    hint="See apps/common/managers.py.",
                    obj=model,
                    id="common.E001",
                )
            )
    return errors


def _has_tenant_id_field(model: Any) -> bool:
    return any(getattr(field, "name", None) == "tenant_id" for field in model._meta.get_fields())
