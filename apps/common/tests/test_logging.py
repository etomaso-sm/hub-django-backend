"""Tests for x-xray-session middleware and the JSON formatter."""

import json
import logging
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from apps.common.logging import JsonFormatter
from apps.common.middleware.xray import (
    XraySessionMiddleware,
    _xray_session,
    get_current_xray_session,
)


def _view_ok(_: Any) -> HttpResponse:
    return HttpResponse(b"ok")


def _view_raises(_: Any) -> HttpResponse:
    raise RuntimeError("explosion")


# ---------- xray session ----------


def test_middleware_uses_header_when_present() -> None:
    captured: dict[str, Any] = {}

    def view(request: Any) -> HttpResponse:
        captured["xray"] = request.xray_session
        captured["via_contextvar"] = get_current_xray_session()
        return HttpResponse(b"ok")

    request = RequestFactory().get("/x", HTTP_X_XRAY_SESSION="xray-existing-123")
    XraySessionMiddleware(view)(request)

    assert captured["xray"] == "xray-existing-123"
    assert captured["via_contextvar"] == "xray-existing-123"


def test_middleware_generates_xray_session_when_absent() -> None:
    captured: dict[str, Any] = {}

    def view(request: Any) -> HttpResponse:
        captured["xray"] = request.xray_session
        return HttpResponse(b"ok")

    request = RequestFactory().get("/x")
    XraySessionMiddleware(view)(request)

    assert captured["xray"] is not None
    assert captured["xray"].startswith("xray-")


def test_middleware_resets_contextvar_after_request() -> None:
    request = RequestFactory().get("/x", HTTP_X_XRAY_SESSION="xray-test")
    XraySessionMiddleware(_view_ok)(request)
    assert _xray_session.get() is None


def test_middleware_resets_contextvar_even_on_exception() -> None:
    request = RequestFactory().get("/x", HTTP_X_XRAY_SESSION="xray-test")
    with pytest.raises(RuntimeError, match="explosion"):
        XraySessionMiddleware(_view_raises)(request)
    assert _xray_session.get() is None


# ---------- structured log ----------


def test_middleware_emits_structured_log_on_success() -> None:
    request = RequestFactory().get("/x", HTTP_X_XRAY_SESSION="xray-test")
    request.user = SimpleNamespace(email="alice@example.com")
    request.tenant_id = "hub_a"

    with patch("apps.common.middleware.xray.logger") as mock_logger:
        XraySessionMiddleware(_view_ok)(request)

    mock_logger.info.assert_called_once()
    call = mock_logger.info.call_args
    assert call.args[0] == "request"
    extra = call.kwargs["extra"]
    assert extra["method"] == "GET"
    assert extra["path"] == "/x"
    assert extra["tenant_id"] == "hub_a"
    assert extra["user_email"] == "alice@example.com"
    assert extra["xray_session"] == "xray-test"
    assert extra["status"] == 200
    assert isinstance(extra["duration_ms"], int)
    # No error field on the happy path.
    assert "error" not in extra


def test_middleware_emits_error_log_on_exception() -> None:
    request = RequestFactory().get("/x", HTTP_X_XRAY_SESSION="xray-test")

    with (
        patch("apps.common.middleware.xray.logger") as mock_logger,
        pytest.raises(RuntimeError, match="explosion"),
    ):
        XraySessionMiddleware(_view_raises)(request)

    mock_logger.error.assert_called_once()
    extra = mock_logger.error.call_args.kwargs["extra"]
    assert extra["status"] == 500
    assert "RuntimeError" in extra["error"]
    assert "explosion" in extra["error"]


def test_middleware_emits_log_without_user_or_tenant() -> None:
    """Anonymous requests (no auth, no tenant middleware upstream) still log."""
    request = RequestFactory().get("/x")

    with patch("apps.common.middleware.xray.logger") as mock_logger:
        XraySessionMiddleware(_view_ok)(request)

    extra = mock_logger.info.call_args.kwargs["extra"]
    assert extra["user_email"] is None
    assert extra["tenant_id"] is None
    assert extra["status"] == 200


# ---------- JSON formatter ----------


def test_json_formatter_emits_single_line_json() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="hub.request",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request",
        args=(),
        exc_info=None,
    )
    record.method = "GET"
    record.path = "/x"
    record.status = 200
    record.duration_ms = 42
    record.xray_session = "xray-abc"
    record.tenant_id = "hub_a"
    record.user_email = "u@e.test"

    out = formatter.format(record)
    parsed = json.loads(out)
    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "hub.request"
    assert parsed["message"] == "request"
    assert parsed["method"] == "GET"
    assert parsed["path"] == "/x"
    assert parsed["status"] == 200
    assert parsed["duration_ms"] == 42
    assert parsed["xray_session"] == "xray-abc"
    assert parsed["tenant_id"] == "hub_a"
    assert parsed["user_email"] == "u@e.test"


def test_json_formatter_omits_absent_fields() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="hub.request",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="plain",
        args=(),
        exc_info=None,
    )
    out = formatter.format(record)
    parsed = json.loads(out)
    assert parsed["message"] == "plain"
    assert "method" not in parsed
    assert "status" not in parsed
