"""Tests for TKT-023 core auth/session routes."""

from collections.abc import Generator
from typing import Any, cast

import pytest
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.auth.models import People, Session, UserTenants
from apps.common.middleware.tenant import DEFAULT_TENANT, reset_current_tenant, set_current_tenant


@pytest.fixture(autouse=True)
def tenant_context() -> Generator[None, None, None]:
    token = set_current_tenant(DEFAULT_TENANT)
    try:
        yield
    finally:
        reset_current_tenant(token)


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def staff(db: Any) -> People:
    return _make_person("staff@local.test", "staff", "Staff User")


@pytest.mark.django_db
def test_login_writes_session_and_tenant_cookies(client: APIClient, staff: People) -> None:
    _make_membership(staff.email, "staff", is_admin=True)

    with override_settings(DEBUG=True):
        response = client.post("/api/auth/login", {"email": staff.email}, format="json")

    assert response.status_code == 200
    assert response.json()["data"]["email"] == staff.email
    assert "hub_session" in response.cookies
    assert "hub_context" in response.cookies
    assert response.cookies["hub_context"].value == DEFAULT_TENANT
    assert Session.objects.filter(person=staff).exists()


@pytest.mark.django_db
def test_login_is_disabled_when_debug_is_false(client: APIClient, staff: People) -> None:
    with override_settings(DEBUG=False):
        response = client.post("/api/auth/login", {"email": staff.email}, format="json")

    assert response.status_code == 403
    assert response.json() == {"ok": False, "error": "local_login_disabled"}


@pytest.mark.django_db
def test_session_me_tenants_and_hub_routes(client: APIClient, staff: People) -> None:
    _make_membership(staff.email, "staff", is_admin=True)

    with override_settings(DEBUG=True):
        login_response = client.post("/api/auth/login", {"email": staff.email}, format="json")
        assert login_response.status_code == 200

        session_response = client.get("/api/auth/session")
        me_response = client.get("/api/me")
        tenants_response = client.get("/api/tenants")
        hub_list_response = client.get("/api/hub/list")
        current_response = client.get("/api/hub/current")
        switch_response = client.post(
            "/api/hub/switch",
            {"hub_id": DEFAULT_TENANT},
            format="json",
        )

    assert session_response.status_code == 200
    assert session_response.json()["data"] == {
        "email": staff.email,
        "name": "Staff User",
        "display_name": "Staff User",
        "role": "staff",
        "source": "session",
        "tenant_id": DEFAULT_TENANT,
    }
    assert me_response.status_code == 200
    assert me_response.json()["data"]["display_name"] == "Staff User"
    assert me_response.json()["data"]["is_admin"] is True
    assert tenants_response.status_code == 200
    assert tenants_response.json()["data"][0]["tenant_id"] == DEFAULT_TENANT
    assert hub_list_response.status_code == 200
    assert hub_list_response.json()["data"][0]["id"] == DEFAULT_TENANT
    assert current_response.status_code == 200
    assert current_response.json()["data"]["hub_id"] == DEFAULT_TENANT
    assert switch_response.status_code == 200
    assert switch_response.cookies["hub_context"].value == DEFAULT_TENANT


@pytest.mark.django_db
def test_signup_creates_person_and_membership(client: APIClient) -> None:
    response = client.post(
        "/api/signup",
        {"email": "founder@example.com", "company_name": "Acme Labs", "name": "Founder"},
        format="json",
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["tenant_id"] == "acme_labs"
    assert People._base_manager.filter(email="founder@example.com").exists()
    assert UserTenants._base_manager.filter(
        user_email="founder@example.com",
        tenant_id="acme_labs",
    ).exists()


def _make_person(email: str, role: str, display_name: str) -> People:
    now = timezone.now()
    return cast(
        People,
        People.objects.create(
            id=f"person-{email.split('@')[0]}",
            email=email,
            display_name=display_name,
            role=role,
            tier="internal",
            entity_access=[],
            scopes=[],
            agents=[],
            status="active",
            monitoring_tier="standard",
            created_at=now,
            updated_at=now,
            tenant_id=DEFAULT_TENANT,
            is_workspace_admin=1,
        ),
    )


def _make_membership(email: str, role: str, is_admin: bool) -> UserTenants:
    now = timezone.now()
    return cast(
        UserTenants,
        UserTenants.objects.create(
            id=f"tenant-{email.split('@')[0]}",
            user_email=email,
            tenant_id=DEFAULT_TENANT,
            role=role,
            is_owner=0,
            is_admin=1 if is_admin else 0,
            joined_at=now,
            access_tier=2 if is_admin else 1,
            ui_mode="standard",
        ),
    )
