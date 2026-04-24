"""x-xray-session passthrough + per-request structured log.

The frontend sends ``x-xray-session`` on every request (an opaque tracing id
generated once per page load). The middleware:

1. Reads the header (or generates one if absent, so every request has a
   session id in logs even for direct / server-to-server calls).
2. Stashes it on ``request.xray_session`` and a contextvar so loggers called
   anywhere inside the request can reference it.
3. On response, emits one structured log record to ``hub.request`` with
   method, path, tenant_id, user_email, xray_session, status, duration_ms.

The JSON formatter lives in ``apps.common.logging``. The handler is wired in
``hub/settings/base.py`` LOGGING.
"""

import logging
import time
import uuid
from collections.abc import Callable
from contextvars import ContextVar, Token
from typing import Any

from django.http import HttpRequest, HttpResponse

_xray_session: ContextVar[str | None] = ContextVar("xray_session", default=None)

logger = logging.getLogger("hub.request")


def get_current_xray_session() -> str | None:
    """Return the active xray session id, or None outside a request."""
    return _xray_session.get()


class XraySessionMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        xray = request.headers.get("x-xray-session") or _generate_xray_session()
        request.xray_session = xray
        token: Token[str | None] = _xray_session.set(xray)
        start = time.perf_counter()
        try:
            response = self.get_response(request)
            self._log_request(request, status=response.status_code, start=start, xray=xray)
            return response
        except Exception as exc:
            self._log_request(
                request,
                status=500,
                start=start,
                xray=xray,
                error=f"{type(exc).__name__}: {exc}",
            )
            raise
        finally:
            _xray_session.reset(token)

    @staticmethod
    def _log_request(
        request: HttpRequest,
        *,
        status: int,
        start: float,
        xray: str,
        error: str | None = None,
    ) -> None:
        duration_ms = int((time.perf_counter() - start) * 1000)
        user = getattr(request, "user", None)
        user_email = getattr(user, "email", None) if user is not None else None
        tenant_id = getattr(request, "tenant_id", None)
        extra: dict[str, Any] = {
            "method": request.method,
            "path": request.path,
            "tenant_id": tenant_id,
            "user_email": user_email,
            "xray_session": xray,
            "status": status,
            "duration_ms": duration_ms,
        }
        if error:
            extra["error"] = error
            logger.error("request", extra=extra)
        else:
            logger.info("request", extra=extra)


def _generate_xray_session() -> str:
    return f"xray-{int(time.time())}-{uuid.uuid4().hex[:6]}"
