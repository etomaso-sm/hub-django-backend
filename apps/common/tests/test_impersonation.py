"""Tests for ImpersonationMiddleware (superadmin-only)."""

import json
from types import SimpleNamespace
from typing import Any

from django.http import HttpResponse
from django.test import RequestFactory

from apps.common.middleware.impersonation import ImpersonationMiddleware


def _view_capturing(captured: dict[str, Any]) -> Any:
    def view(request: Any) -> HttpResponse:
        captured["impersonate_as"] = getattr(request, "impersonate_as", "<not set>")
        return HttpResponse(b"ok")

    return view


def _request_with_user(path: str, role: str | None, authenticated: bool = True) -> Any:
    req = RequestFactory().get(path)
    # Simulate what AuthenticationMiddleware would set.
    req.user = SimpleNamespace(is_authenticated=authenticated, role=role)
    return req


def test_no_impersonate_param_sets_attribute_to_none() -> None:
    captured: dict[str, Any] = {}
    middleware = ImpersonationMiddleware(_view_capturing(captured))
    req = _request_with_user("/x", role="normal")
    response = middleware(req)
    assert response.status_code == 200
    assert captured["impersonate_as"] is None


def test_superadmin_can_impersonate_and_attribute_is_set() -> None:
    captured: dict[str, Any] = {}
    middleware = ImpersonationMiddleware(_view_capturing(captured))
    req = _request_with_user("/x?impersonate=target@example.com", role="superadmin")
    # Append query param via RequestFactory overrides.
    req = RequestFactory().get("/x", {"impersonate": "target@example.com"})
    req.user = SimpleNamespace(is_authenticated=True, role="superadmin")
    response = middleware(req)
    assert response.status_code == 200
    assert captured["impersonate_as"] == "target@example.com"


def test_normal_user_attempting_impersonation_gets_403() -> None:
    captured: dict[str, Any] = {}
    middleware = ImpersonationMiddleware(_view_capturing(captured))
    req = RequestFactory().get("/x", {"impersonate": "target@example.com"})
    req.user = SimpleNamespace(is_authenticated=True, role="normal")
    response = middleware(req)
    assert response.status_code == 403
    body = json.loads(response.content)
    assert body == {"ok": False, "error": "impersonation not allowed"}
    # View must not have been called.
    assert "impersonate_as" not in captured


def test_staff_user_attempting_impersonation_gets_403() -> None:
    captured: dict[str, Any] = {}
    middleware = ImpersonationMiddleware(_view_capturing(captured))
    req = RequestFactory().get("/x", {"impersonate": "target@example.com"})
    req.user = SimpleNamespace(is_authenticated=True, role="staff")
    response = middleware(req)
    assert response.status_code == 403
    body = json.loads(response.content)
    assert body == {"ok": False, "error": "impersonation not allowed"}
    assert "impersonate_as" not in captured


def test_unauthenticated_attempting_impersonation_gets_403() -> None:
    captured: dict[str, Any] = {}
    middleware = ImpersonationMiddleware(_view_capturing(captured))
    req = RequestFactory().get("/x", {"impersonate": "target@example.com"})
    req.user = SimpleNamespace(is_authenticated=False, role=None)
    response = middleware(req)
    assert response.status_code == 403
    body = json.loads(response.content)
    assert body == {"ok": False, "error": "impersonation not allowed"}


def test_missing_user_attribute_gets_403() -> None:
    """If AuthenticationMiddleware hasn't run for some reason, deny rather than crash."""
    captured: dict[str, Any] = {}
    middleware = ImpersonationMiddleware(_view_capturing(captured))
    req = RequestFactory().get("/x", {"impersonate": "target@example.com"})
    # deliberately DO NOT set req.user
    response = middleware(req)
    assert response.status_code == 403
    body = json.loads(response.content)
    assert body == {"ok": False, "error": "impersonation not allowed"}
