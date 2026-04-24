"""Hub exception handler + raw_response opt-out decorator."""

from collections.abc import Callable
from typing import Any, TypeVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

F = TypeVar("F", bound=Callable[..., Any])


def raw_response(view: F) -> F:
    """Opt a function-based view out of the hub envelope wrapper.

    For class-based views, set ``raw_response = True`` as a class attribute
    instead of using this decorator.
    """
    view._raw_response = True  # type: ignore[attr-defined]
    return view


def hub_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """Emit errors as ``{"ok": false, "error": "<msg>"}`` with correct status.

    Delegates to DRF's default handler first, then rewraps the body. For
    exceptions the default handler does not recognize (returns None), we
    synthesize a 500 response with a generic error string.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        return Response(
            {"ok": False, "error": "internal_server_error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = _extract_message(response.data)
    response.data = {"ok": False, "error": message}
    return response


def _extract_message(detail: Any) -> str:
    """Pull a single error string out of DRF's varied error shapes."""
    if isinstance(detail, str):
        return detail
    if isinstance(detail, dict):
        if "detail" in detail:
            return str(detail["detail"])
        for key, value in detail.items():
            if isinstance(value, list) and value:
                return f"{key}: {value[0]}"
            return f"{key}: {value}"
    if isinstance(detail, list) and detail:
        return str(detail[0])
    return "error"
