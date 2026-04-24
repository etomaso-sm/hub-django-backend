"""Tenant resolution middleware + contextvar-backed current-tenant accessor.

Every request carries `?tenant=<id>`. The middleware reads it, falls back to
``DEFAULT_TENANT`` when absent, stashes the value on `request.tenant_id`, and
sets a module-level contextvar so `TenantScopedManager` (and any other code
running inside the request) can scope queries by the active tenant.

The contextvar is reset at request end to prevent leakage across concurrent
async requests under ASGI.
"""

from collections.abc import Callable
from contextvars import ContextVar, Token

from django.http import HttpRequest, HttpResponse

DEFAULT_TENANT = "sprint_mode"

_current_tenant: ContextVar[str | None] = ContextVar("current_tenant", default=None)


class TenantNotSetError(RuntimeError):
    """Raised when tenant-scoped code runs outside a tenant-aware context."""


def get_current_tenant() -> str:
    """Return the tenant ID active in the current request context.

    Raises ``TenantNotSetError`` when called outside a request (e.g. in a
    management command or a Celery task that forgot to set the tenant). Each
    caller must decide whether to catch this or let it surface as a bug.
    """
    tenant = _current_tenant.get()
    if tenant is None:
        raise TenantNotSetError("get_current_tenant() called outside a tenant-aware context")
    return tenant


def set_current_tenant(tenant_id: str) -> Token[str | None]:
    """Set the current tenant. Returns a token the caller can use to reset."""
    return _current_tenant.set(tenant_id)


def reset_current_tenant(token: Token[str | None]) -> None:
    """Reset the contextvar to its prior value (use the token from set_current_tenant)."""
    _current_tenant.reset(token)


class TenantMiddleware:
    """Resolve the active tenant from ``?tenant=`` and bind it for the request.

    Request attribute set:
        ``request.tenant_id: str``   always populated (falls back to DEFAULT_TENANT).

    Contextvar set:
        Visible to any code that calls ``get_current_tenant()`` during the
        request. Reset on response, including on exceptions.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        tenant = request.GET.get("tenant") or DEFAULT_TENANT
        request.tenant_id = tenant
        token = _current_tenant.set(tenant)
        try:
            return self.get_response(request)
        finally:
            _current_tenant.reset(token)
