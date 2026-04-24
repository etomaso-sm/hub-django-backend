"""Tests for HubAuthentication (DRF auth backend)."""

from datetime import timedelta
from typing import Any, cast
from unittest.mock import patch

import jwt as pyjwt
import pytest
from django.test import RequestFactory, override_settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from apps.auth.authentication import HubAuthentication
from apps.auth.models import People

Session: Any = None

pytestmark = pytest.mark.skip(
    reason="TKT-020 replaces auth models from inspectdb; TKT-023 ports core auth/session."
)


@pytest.fixture
def person(db: Any) -> People:
    return cast(People, People.objects.create(email="alice@example.com", role="normal"))


@pytest.fixture
def staff(db: Any) -> People:
    return cast(People, People.objects.create(email="staff@example.com", role="staff"))


# ---------- no credentials ----------


@pytest.mark.django_db
def test_no_credentials_returns_none() -> None:
    request = RequestFactory().get("/x")
    assert HubAuthentication().authenticate(request) is None


# ---------- DEV_BYPASS_AUTH_AS_EMAIL ----------


@pytest.mark.django_db
def test_dev_bypass_in_debug_resolves_user(person: People) -> None:
    with override_settings(DEBUG=True, DEV_BYPASS_AUTH_AS_EMAIL="alice@example.com"):
        result = HubAuthentication().authenticate(RequestFactory().get("/x"))
    assert result is not None
    user, _ = result
    assert user.email == "alice@example.com"


@pytest.mark.django_db
def test_dev_bypass_ignored_when_not_debug(person: People) -> None:
    with override_settings(DEBUG=False, DEV_BYPASS_AUTH_AS_EMAIL="alice@example.com"):
        assert HubAuthentication().authenticate(RequestFactory().get("/x")) is None


@pytest.mark.django_db
def test_dev_bypass_unknown_email_raises() -> None:
    with (
        override_settings(DEBUG=True, DEV_BYPASS_AUTH_AS_EMAIL="ghost@example.com"),
        pytest.raises(AuthenticationFailed, match="unknown_user"),
    ):
        HubAuthentication().authenticate(RequestFactory().get("/x"))


# ---------- CF Access email header (no JWT) ----------


@pytest.mark.django_db
def test_cf_access_email_header_resolves_user(person: People) -> None:
    request = RequestFactory().get(
        "/x", HTTP_CF_ACCESS_AUTHENTICATED_USER_EMAIL="alice@example.com"
    )
    result = HubAuthentication().authenticate(request)
    assert result is not None
    user, _ = result
    assert user.email == "alice@example.com"


@pytest.mark.django_db
def test_cf_access_email_header_unknown_raises() -> None:
    request = RequestFactory().get(
        "/x", HTTP_CF_ACCESS_AUTHENTICATED_USER_EMAIL="ghost@example.com"
    )
    with pytest.raises(AuthenticationFailed, match="unknown_user"):
        HubAuthentication().authenticate(request)


# ---------- CF Access JWT ----------


@pytest.mark.django_db
def test_cf_access_valid_jwt_resolves_user(person: People) -> None:
    request = RequestFactory().get("/x", HTTP_CF_ACCESS_JWT_ASSERTION="fake.jwt.token")
    with (
        override_settings(
            CF_ACCESS_JWKS_URL="https://example.test/jwks",
            CF_ACCESS_AUD="hub-audience",
        ),
        patch(
            "apps.auth.authentication.verify_cf_access_jwt",
            return_value={"email": "alice@example.com"},
        ),
    ):
        result = HubAuthentication().authenticate(request)
    assert result is not None
    user, _ = result
    assert user.email == "alice@example.com"


@pytest.mark.django_db
def test_cf_access_invalid_jwt_raises() -> None:
    request = RequestFactory().get("/x", HTTP_CF_ACCESS_JWT_ASSERTION="bad.jwt")
    with (
        override_settings(
            CF_ACCESS_JWKS_URL="https://example.test/jwks",
            CF_ACCESS_AUD="hub-audience",
        ),
        patch(
            "apps.auth.authentication.verify_cf_access_jwt",
            side_effect=pyjwt.InvalidTokenError("bad signature"),
        ),
        pytest.raises(AuthenticationFailed, match="cf_access_jwt_invalid"),
    ):
        HubAuthentication().authenticate(request)


@pytest.mark.django_db
def test_cf_access_misconfigured_raises() -> None:
    """JWT present but settings missing — fail loudly, do not silently pass."""
    request = RequestFactory().get("/x", HTTP_CF_ACCESS_JWT_ASSERTION="jwt")
    with (
        override_settings(CF_ACCESS_JWKS_URL=None, CF_ACCESS_AUD=None),
        pytest.raises(AuthenticationFailed, match="cf_access_not_configured"),
    ):
        HubAuthentication().authenticate(request)


# ---------- hub_session cookie ----------


@pytest.mark.django_db
def test_hub_session_cookie_resolves_user(person: People) -> None:
    Session.objects.create(
        token="abc123",
        person=person,
        expires_at=timezone.now() + timedelta(days=7),
    )
    request = RequestFactory().get("/x")
    request.COOKIES["hub_session"] = "abc123"
    result = HubAuthentication().authenticate(request)
    assert result is not None
    user, _ = result
    assert user.pk == person.pk


@pytest.mark.django_db
def test_hub_session_expired_raises(person: People) -> None:
    Session.objects.create(
        token="expired",
        person=person,
        expires_at=timezone.now() - timedelta(days=1),
    )
    request = RequestFactory().get("/x")
    request.COOKIES["hub_session"] = "expired"
    with pytest.raises(AuthenticationFailed, match="session_expired"):
        HubAuthentication().authenticate(request)


@pytest.mark.django_db
def test_hub_session_unknown_token_raises() -> None:
    request = RequestFactory().get("/x")
    request.COOKIES["hub_session"] = "nope"
    with pytest.raises(AuthenticationFailed, match="session_invalid"):
        HubAuthentication().authenticate(request)


# ---------- service token ----------


@pytest.mark.django_db
def test_service_token_resolves_user(person: People) -> None:
    request = RequestFactory().get("/x", HTTP_AUTHORIZATION="Bearer svc_token_1")
    with override_settings(SERVICE_TOKENS={"svc_token_1": "alice@example.com"}):
        result = HubAuthentication().authenticate(request)
    assert result is not None
    user, _ = result
    assert user.email == "alice@example.com"


@pytest.mark.django_db
def test_service_token_unknown_raises() -> None:
    request = RequestFactory().get("/x", HTTP_AUTHORIZATION="Bearer nope")
    with (
        override_settings(SERVICE_TOKENS={}),
        pytest.raises(AuthenticationFailed, match="service_token_invalid"),
    ):
        HubAuthentication().authenticate(request)


@pytest.mark.django_db
def test_non_bearer_authorization_header_ignored() -> None:
    """A Basic / Digest / other scheme should not be interpreted as a service token."""
    request = RequestFactory().get("/x", HTTP_AUTHORIZATION="Basic anything")
    assert HubAuthentication().authenticate(request) is None
