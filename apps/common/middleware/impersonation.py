"""Impersonation middleware. Superadmin-only.

Reads ``?impersonate=<email>`` from the request. If present:

- If the caller is a superadmin (``request.user.role == "superadmin"``),
  sets ``request.impersonate_as`` to the target email and stubs an audit
  write (finalized in TKT-045, which ports the audit app).
- Otherwise returns 403 with the envelope ``{"ok": false, "error": "impersonation not allowed"}``.

When ``?impersonate`` is absent, ``request.impersonate_as`` is set to None
so downstream code can always read the attribute safely.
"""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse


class ImpersonationMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        target = request.GET.get("impersonate")

        if target is None:
            request.impersonate_as = None
            return self.get_response(request)

        user = getattr(request, "user", None)
        authenticated = bool(user is not None and getattr(user, "is_authenticated", False))
        role = getattr(user, "role", None)

        if not authenticated or role != "superadmin":
            return JsonResponse(
                {"ok": False, "error": "impersonation not allowed"},
                status=403,
            )

        request.impersonate_as = target
        _audit_impersonation_stub(request, target)
        return self.get_response(request)


def _audit_impersonation_stub(request: HttpRequest, target: str) -> None:
    """Stub for the audit-write that lands in TKT-045.

    TODO(TKT-045): write a row to the `audit_log` / `stream_entries` table
    capturing the superadmin who impersonated, the target email, the
    xray_session, and the timestamp.
    """
    # Intentionally a no-op until the audit app is ported. Kept as a function
    # (not inline) so TKT-045 can replace the body without touching the
    # middleware's control flow.
    return
