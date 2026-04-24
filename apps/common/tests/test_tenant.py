"""Tests for TenantMiddleware, contextvar accessors, TenantScopedManager,
and the system check that enforces manager discipline."""

from typing import Any
from unittest.mock import MagicMock

import pytest
from django.core.checks import Error
from django.http import HttpResponse
from django.test import RequestFactory

from apps.common.checks import check_tenant_managers
from apps.common.managers import TenantScopedManager
from apps.common.middleware.tenant import (
    DEFAULT_TENANT,
    TenantMiddleware,
    TenantNotSetError,
    _current_tenant,
    get_current_tenant,
    reset_current_tenant,
    set_current_tenant,
)

# ---------- contextvar + accessors ----------


def test_get_current_tenant_raises_outside_context() -> None:
    # Ensure clean slate (tests may leak otherwise).
    assert _current_tenant.get() is None
    with pytest.raises(TenantNotSetError):
        get_current_tenant()


def test_set_and_get_current_tenant_round_trip() -> None:
    token = set_current_tenant("hub_a")
    try:
        assert get_current_tenant() == "hub_a"
    finally:
        reset_current_tenant(token)
    assert _current_tenant.get() is None


# ---------- middleware ----------


def test_middleware_reads_tenant_from_query_param() -> None:
    captured: dict[str, Any] = {}

    def view(request: Any) -> HttpResponse:
        captured["tenant_id"] = request.tenant_id
        captured["current"] = get_current_tenant()
        return HttpResponse(b"ok")

    middleware = TenantMiddleware(view)
    request = RequestFactory().get("/x", {"tenant": "hub_a"})
    response = middleware(request)

    assert response.status_code == 200
    assert captured["tenant_id"] == "hub_a"
    assert captured["current"] == "hub_a"


def test_middleware_falls_back_to_default_when_absent() -> None:
    captured: dict[str, Any] = {}

    def view(request: Any) -> HttpResponse:
        captured["current"] = get_current_tenant()
        return HttpResponse(b"ok")

    middleware = TenantMiddleware(view)
    request = RequestFactory().get("/x")
    middleware(request)

    assert captured["current"] == DEFAULT_TENANT


def test_middleware_resets_contextvar_after_request() -> None:
    def view(_: Any) -> HttpResponse:
        return HttpResponse(b"ok")

    middleware = TenantMiddleware(view)
    middleware(RequestFactory().get("/x", {"tenant": "hub_a"}))

    # Outside the request scope the contextvar must be unset.
    assert _current_tenant.get() is None


def test_middleware_resets_contextvar_even_on_exception() -> None:
    def view(_: Any) -> HttpResponse:
        raise RuntimeError("boom")

    middleware = TenantMiddleware(view)
    with pytest.raises(RuntimeError, match="boom"):
        middleware(RequestFactory().get("/x", {"tenant": "hub_a"}))

    assert _current_tenant.get() is None


# ---------- TenantScopedManager ----------


def test_manager_get_queryset_applies_tenant_filter() -> None:
    """TenantScopedManager.get_queryset should filter by the current tenant.

    We mock the parent's get_queryset since we do not need a real model to
    prove the filter is added (full DB-level fuzz lands in the first ticket
    that introduces a tenant-scoped model).
    """
    token = set_current_tenant("hub_a")
    try:
        mgr = TenantScopedManager()
        fake_parent_qs = MagicMock(name="parent_qs")
        fake_parent_qs.filter.return_value = "filtered"
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "django.db.models.Manager.get_queryset",
                lambda self: fake_parent_qs,
            )
            result = mgr.get_queryset()
        assert result == "filtered"
        fake_parent_qs.filter.assert_called_once_with(tenant_id="hub_a")
    finally:
        reset_current_tenant(token)


def test_manager_raises_when_tenant_not_set() -> None:
    mgr = TenantScopedManager()
    with pytest.raises(TenantNotSetError):
        # Trigger get_queryset() with no tenant set in context.
        mgr.get_queryset()


# ---------- system check ----------


def test_check_flags_misconfigured_model() -> None:
    """check_tenant_managers must return an Error for a managed model with a
    tenant_id field that does NOT use TenantScopedManager."""
    bad_model = _make_fake_model(
        label="common.BadModel",
        managed=True,
        has_tenant_id=True,
        manager=MagicMock(name="wrong_manager"),
    )

    errors = _run_check_with_models([bad_model])
    assert any(
        isinstance(e, Error) and e.id == "common.E001" for e in errors
    ), f"expected common.E001, got: {errors}"


def test_check_ignores_unmanaged_model() -> None:
    unmanaged = _make_fake_model(
        label="common.UnmanagedModel",
        managed=False,
        has_tenant_id=True,
        manager=MagicMock(name="wrong_manager"),
    )

    errors = _run_check_with_models([unmanaged])
    assert not any(
        getattr(e, "id", None) == "common.E001" for e in errors
    ), "should not flag unmanaged models"


def test_check_ignores_model_without_tenant_id() -> None:
    no_tenant = _make_fake_model(
        label="common.Global",
        managed=True,
        has_tenant_id=False,
        manager=MagicMock(name="wrong_manager"),
    )

    errors = _run_check_with_models([no_tenant])
    assert not any(
        getattr(e, "id", None) == "common.E001" for e in errors
    ), "should not flag global (no tenant_id) models"


def test_check_accepts_correct_manager() -> None:
    ok_model = _make_fake_model(
        label="common.GoodModel",
        managed=True,
        has_tenant_id=True,
        manager=TenantScopedManager(),
    )

    errors = _run_check_with_models([ok_model])
    assert not any(
        getattr(e, "id", None) == "common.E001" for e in errors
    ), "model using TenantScopedManager must pass"


# ---------- helpers ----------


def _make_fake_model(*, label: str, managed: bool, has_tenant_id: bool, manager: Any) -> Any:
    """Build a lightweight stand-in for a Django model with the shape the
    check inspects: `_meta.managed`, `_meta.get_fields()`, `_meta.label`,
    and `_default_manager`."""
    fields = []
    if has_tenant_id:
        f = MagicMock(name="tenant_id_field")
        f.name = "tenant_id"
        fields.append(f)
    meta = MagicMock(name=f"{label}.meta")
    meta.managed = managed
    meta.label = label
    meta.get_fields.return_value = fields
    model = MagicMock(name=label)
    model._meta = meta
    model._default_manager = manager
    return model


def _run_check_with_models(fake_models: list[Any]) -> list[Any]:
    """Run check_tenant_managers with django.apps.get_models patched to the
    given fakes. Returns the list of messages."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("django.apps.apps.get_models", lambda: fake_models)
        return list(check_tenant_managers(None))
