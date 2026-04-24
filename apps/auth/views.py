# mypy: disable-error-code=misc
"""Core auth/session/me routes ported for TKT-023."""

from __future__ import annotations

import secrets
import uuid
from datetime import timedelta
from typing import Any, cast

from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.decorators import api_view
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
)
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.models import People, Session, UserTenants
from apps.common.middleware.tenant import DEFAULT_TENANT

SESSION_TTL = timedelta(days=7)
SESSION_MAX_AGE = int(SESSION_TTL.total_seconds())
HUB_CONTEXT_COOKIE = "hub_context"


@api_view(["GET", "POST"])  # type: ignore[untyped-decorator]
def login(request: Request) -> Response:
    """DEBUG-only local login that mints the Hub session cookie.

    Production auth continues to be handled by CF Access / OAuth callback work.
    This endpoint exists so the strangler stack can exercise the frontend
    without CSRF or a Google OAuth setup.
    """
    if not settings.DEBUG:
        raise PermissionDenied("local_login_disabled")

    person = _resolve_login_person(request)
    session = _create_session(person, request)
    tenant_id = _default_tenant_for(person)
    response = Response(
        {
            "url": _next_url(request),
            "email": person.email,
            "tenant_id": tenant_id,
            "expires_at": session.expires_at.isoformat(),
        }
    )
    _set_login_cookies(response, session.token, tenant_id)
    return response


@api_view(["GET"])  # type: ignore[untyped-decorator]
def auth_session(request: Request) -> Response:
    person = cast(People, request.user)
    return Response(
        {
            "email": person.email,
            "name": person.display_name,
            "display_name": person.display_name,
            "role": person.role,
            "source": _auth_source(request),
            "tenant_id": _default_tenant_for(person),
        }
    )


@api_view(["GET"])  # type: ignore[untyped-decorator]
def me(request: Request) -> Response:
    person = cast(People, request.user)
    return Response(_person_payload(person))


@api_view(["POST"])  # type: ignore[untyped-decorator]
def signup(request: Request) -> Response:
    body = _request_data(request)
    email = _normalize_email(cast(str | None, body.get("email")))
    company_name = str(body.get("company_name") or body.get("company") or "").strip()
    if not email or not company_name:
        raise ValidationError("email and company_name required")

    now = timezone.now()
    tenant_id = _unique_tenant_id(company_name)
    person = _get_or_create_person(
        email=email,
        display_name=str(body.get("name") or body.get("display_name") or email.split("@")[0]),
        tenant_id=tenant_id,
        now=now,
    )
    membership = _get_or_create_membership(
        email=person.email,
        tenant_id=tenant_id,
        role="owner",
        is_owner=True,
        is_admin=True,
        now=now,
    )
    trial_ends = now + timedelta(days=14)
    return Response(
        {
            "tenant_id": tenant_id,
            "status": "provisioning",
            "login_url": f"https://heyhub.ai/?hub={tenant_id}",
            "trial_ends": trial_ends.isoformat(),
            "membership_id": membership.id,
        }
    )


@api_view(["GET"])  # type: ignore[untyped-decorator]
def tenants(request: Request) -> Response:
    person = cast(People, request.user)
    return Response([_tenant_payload(row) for row in _memberships_for(person.email)])


@api_view(["GET"])  # type: ignore[untyped-decorator]
def hub_list(request: Request) -> Response:
    person = cast(People, request.user)
    hubs = []
    for row in _memberships_for(person.email):
        tenant_id = row.tenant_id or DEFAULT_TENANT
        hubs.append(
            {
                "id": tenant_id,
                "tenant_id": tenant_id,
                "name": _tenant_name(tenant_id),
                "hub_type": "company",
                "role": row.role or person.role,
            }
        )
    return Response(hubs)


@api_view(["GET"])  # type: ignore[untyped-decorator]
def hub_current(request: Request) -> Response:
    hub_id = request.COOKIES.get(HUB_CONTEXT_COOKIE) or DEFAULT_TENANT
    return Response({"hub_id": hub_id, "hostname": request.get_host()})


@api_view(["POST"])  # type: ignore[untyped-decorator]
def hub_switch(request: Request) -> Response:
    person = cast(People, request.user)
    body = _request_data(request)
    hub_id = str(body.get("hub_id") or "").strip()
    if not hub_id:
        raise ValidationError("hub_id required")
    if hub_id != DEFAULT_TENANT and not _has_membership(person.email, hub_id):
        raise PermissionDenied("access denied")

    response = Response({"hub_id": hub_id, "name": _tenant_name(hub_id)})
    _set_hub_context_cookie(response, hub_id)
    return response


def _request_data(request: Request) -> dict[str, Any]:
    data = request.data
    if isinstance(data, dict):
        return cast(dict[str, Any], data)
    return {}


def _resolve_login_person(request: Request) -> People:
    body = _request_data(request)
    email = _normalize_email(
        cast(str | None, body.get("email"))
        or request.query_params.get("email")
        or getattr(settings, "DEV_BYPASS_AUTH_AS_EMAIL", None)
    )
    if not email:
        raise ValidationError("email required")
    try:
        return cast(People, People.objects.get(email=email))
    except People.DoesNotExist as exc:
        raise AuthenticationFailed(f"unknown_user: {email}") from exc


def _normalize_email(raw: str | None) -> str:
    return (raw or "").strip().lower()


def _next_url(request: Request) -> str:
    value = request.query_params.get("next") or "/brief"
    return value if value.startswith("/") and not value.startswith("//") else "/brief"


def _create_session(person: People, request: Request) -> Session:
    now = timezone.now()
    token = secrets.token_urlsafe(32)
    while Session.objects.filter(token=token).exists():
        token = secrets.token_urlsafe(32)
    return cast(
        Session,
        Session.objects.create(
            token=token,
            person=person,
            created_at=now,
            expires_at=now + SESSION_TTL,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        ),
    )


def _set_login_cookies(response: Response, session_token: str, tenant_id: str) -> None:
    secure = not settings.DEBUG
    response.set_cookie(
        getattr(settings, "SESSION_COOKIE_NAME", "hub_session"),
        session_token,
        max_age=SESSION_MAX_AGE,
        path="/",
        secure=secure,
        httponly=True,
        samesite="Lax",
    )
    _set_hub_context_cookie(response, tenant_id)


def _set_hub_context_cookie(response: Response, tenant_id: str) -> None:
    response.set_cookie(
        HUB_CONTEXT_COOKIE,
        tenant_id,
        max_age=365 * 24 * 60 * 60,
        path="/",
        secure=not settings.DEBUG,
        httponly=False,
        samesite="Lax",
    )


def _auth_source(request: Request) -> str:
    if settings.DEBUG and getattr(settings, "DEV_BYPASS_AUTH_AS_EMAIL", None):
        return "dev"
    if request.META.get("HTTP_CF_ACCESS_JWT_ASSERTION") or request.META.get(
        "HTTP_CF_ACCESS_AUTHENTICATED_USER_EMAIL"
    ):
        return "cf-access"
    if request.COOKIES.get(getattr(settings, "SESSION_COOKIE_NAME", "hub_session")):
        return "session"
    if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer "):
        return "service-token"
    return "unknown"


def _person_payload(person: People) -> dict[str, Any]:
    membership = _primary_membership(person)
    tenant_id = (
        membership.tenant_id if membership is not None else person.tenant_id
    ) or DEFAULT_TENANT
    ui_mode = "standard"
    if membership is not None and membership.ui_mode:
        ui_mode = membership.ui_mode
    is_membership_admin = bool(membership and membership.is_admin)
    is_staffish = person.role in ("staff", "superadmin")
    return {
        "id": person.id,
        "email": person.email,
        "name": person.display_name,
        "display_name": person.display_name,
        "role": person.role,
        "tier": person.tier,
        "title": person.title,
        "division": person.division,
        "tenant_id": tenant_id,
        "ui_mode": ui_mode,
        "status": person.status,
        "avatar_url": person.avatar_url or person.photo_url,
        "photo_url": person.photo_url or person.avatar_url,
        "is_admin": is_membership_admin or is_staffish,
        "is_workspace_admin": bool(person.is_workspace_admin) or is_staffish,
        "permissions": [],
        "entity_access": person.entity_access or [],
        "scopes": person.scopes or [],
        "agents": person.agents or [],
        "company": {
            "name": _tenant_name(tenant_id),
            "accent_color": "#4F6EF7",
        },
    }


def _primary_membership(person: People) -> UserTenants | None:
    return cast(
        UserTenants | None,
        UserTenants._base_manager.filter(user_email=person.email, tenant_id=person.tenant_id)
        .order_by("tenant_id")
        .first()
        or UserTenants._base_manager.filter(user_email=person.email).order_by("tenant_id").first(),
    )


def _memberships_for(email: str) -> list[UserTenants]:
    rows = list(UserTenants._base_manager.filter(user_email=email).order_by("tenant_id"))
    if rows:
        return cast(list[UserTenants], rows)
    now = timezone.now()
    return [
        UserTenants(
            id="fallback-sprint-mode",
            user_email=email,
            tenant_id=DEFAULT_TENANT,
            role="normal",
            is_owner=0,
            is_admin=0,
            joined_at=now,
            access_tier=1,
            ui_mode="standard",
        )
    ]


def _tenant_payload(row: UserTenants) -> dict[str, Any]:
    tenant_id = row.tenant_id or DEFAULT_TENANT
    return {
        "tenant_id": tenant_id,
        "id": tenant_id,
        "name": _tenant_name(tenant_id),
        "accent_color": "#4F6EF7",
        "logo_url": None,
        "role": row.role,
        "is_owner": bool(row.is_owner),
        "is_admin": bool(row.is_admin),
        "access_tier": row.access_tier,
        "ui_mode": row.ui_mode or "standard",
    }


def _tenant_name(tenant_id: str) -> str:
    if tenant_id == DEFAULT_TENANT:
        return "Sprint Mode"
    return tenant_id.replace("_", " ").replace("-", " ").title()


def _default_tenant_for(person: People) -> str:
    membership = _primary_membership(person)
    return (membership.tenant_id if membership is not None else person.tenant_id) or DEFAULT_TENANT


def _has_membership(email: str, tenant_id: str) -> bool:
    return cast(
        bool,
        UserTenants._base_manager.filter(user_email=email, tenant_id=tenant_id).exists(),
    )


def _unique_tenant_id(company_name: str) -> str:
    base = slugify(company_name).replace("-", "_")[:30].strip("_") or f"hub_{uuid.uuid4().hex[:8]}"
    tenant_id = base
    while UserTenants._base_manager.filter(tenant_id=tenant_id).exists():
        tenant_id = f"{base[:24]}_{uuid.uuid4().hex[:5]}"
    return tenant_id


def _get_or_create_person(email: str, display_name: str, tenant_id: str, now: Any) -> People:
    person, _ = People._base_manager.get_or_create(
        email=email,
        defaults={
            "id": f"person-{uuid.uuid4().hex[:12]}",
            "display_name": display_name,
            "role": "normal",
            "tier": "internal",
            "entity_access": [],
            "scopes": [],
            "agents": [],
            "status": "active",
            "monitoring_tier": "standard",
            "created_at": now,
            "updated_at": now,
            "tenant_id": tenant_id,
        },
    )
    return cast(People, person)


def _get_or_create_membership(
    email: str,
    tenant_id: str,
    role: str,
    is_owner: bool,
    is_admin: bool,
    now: Any,
) -> UserTenants:
    membership, _ = UserTenants._base_manager.get_or_create(
        user_email=email,
        tenant_id=tenant_id,
        defaults={
            "id": f"tenant-{uuid.uuid4().hex[:12]}",
            "role": role,
            "is_owner": int(is_owner),
            "is_admin": int(is_admin),
            "joined_at": now,
            "access_tier": 3 if is_owner else 1,
            "ui_mode": "standard",
        },
    )
    return cast(UserTenants, membership)
