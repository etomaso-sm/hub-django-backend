"""Tests for IsAuthenticatedOrPublic."""

from types import SimpleNamespace
from typing import Any

from django.test import override_settings

from apps.common.permissions import IsAuthenticatedOrPublic


def _request(path: str, authenticated: bool = False) -> Any:
    return SimpleNamespace(
        path=path,
        user=SimpleNamespace(is_authenticated=authenticated),
    )


PUBLIC_SET = [
    "/api/health",
    "/api/health/*",
    "/api/signup",
    "/api/waitlist",
    "/webhooks/stripe",
    "/webhooks/privacy",
    "/portal/*",
    "/booking/*",
    "/a2a/*",
    "/labs/manifest",
    "/api/onboarding/waitlist",
]


def test_authenticated_user_always_allowed() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        req = _request("/api/private", authenticated=True)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is True


def test_unauthenticated_user_denied_on_protected_path() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        req = _request("/api/private", authenticated=False)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is False


def test_unauthenticated_user_allowed_on_exact_public_path() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        req = _request("/api/health", authenticated=False)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is True


def test_unauthenticated_user_allowed_on_wildcard_public_path() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        req = _request("/api/health/full", authenticated=False)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is True


def test_unauthenticated_webhook_allowed() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        req = _request("/webhooks/stripe", authenticated=False)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is True


def test_unauthenticated_portal_wildcard_allowed() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        req = _request("/portal/anything/deep", authenticated=False)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is True


def test_empty_pattern_list_requires_auth_everywhere() -> None:
    with override_settings(PUBLIC_URL_PATTERNS=[]):
        req = _request("/api/health", authenticated=False)
        assert IsAuthenticatedOrPublic().has_permission(req, None) is False


def test_missing_user_attribute_denied_on_protected() -> None:
    req = SimpleNamespace(path="/api/private")  # no `user`
    with override_settings(PUBLIC_URL_PATTERNS=PUBLIC_SET):
        assert IsAuthenticatedOrPublic().has_permission(req, None) is False
