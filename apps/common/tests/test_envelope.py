"""Tests for the hub envelope renderer and exception handler."""

import json

import pytest
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView

from apps.common.exceptions import hub_exception_handler, raw_response
from apps.common.renderers import HubJSONRenderer


def test_renderer_wraps_dict_payload() -> None:
    renderer = HubJSONRenderer()
    out = renderer.render({"name": "alice"})
    assert json.loads(out) == {"ok": True, "data": {"name": "alice"}}


def test_renderer_wraps_list_payload() -> None:
    renderer = HubJSONRenderer()
    out = renderer.render([1, 2, 3])
    assert json.loads(out) == {"ok": True, "data": [1, 2, 3]}


def test_renderer_returns_empty_bytes_for_none() -> None:
    assert HubJSONRenderer().render(None) == b""


def test_renderer_passes_through_already_wrapped_success() -> None:
    out = HubJSONRenderer().render({"ok": True, "data": {"a": 1}})
    assert json.loads(out) == {"ok": True, "data": {"a": 1}}


def test_renderer_passes_through_error_envelope() -> None:
    out = HubJSONRenderer().render({"ok": False, "error": "boom"})
    assert json.loads(out) == {"ok": False, "error": "boom"}


def test_raw_response_decorator_marks_function() -> None:
    @raw_response
    def webhook_view(request: object) -> None:
        return None

    assert getattr(webhook_view, "_raw_response", False) is True


def test_renderer_class_level_opt_out() -> None:
    class StripeWebhookView(APIView):  # type: ignore[misc]  # APIView is untyped
        raw_response = True

    renderer = HubJSONRenderer()
    ctx = {"view": StripeWebhookView(), "request": None}
    out = renderer.render({"stripe_event": "ok"}, renderer_context=ctx)
    assert json.loads(out) == {"stripe_event": "ok"}


@pytest.mark.django_db
def test_exception_handler_not_found() -> None:
    response = hub_exception_handler(NotFound("nope"), {})
    assert response is not None
    assert response.status_code == 404
    assert response.data == {"ok": False, "error": "nope"}


@pytest.mark.django_db
def test_exception_handler_validation_error() -> None:
    response = hub_exception_handler(ValidationError({"email": ["invalid"]}), {})
    assert response is not None
    assert response.status_code == 400
    assert response.data["ok"] is False
    assert "email" in response.data["error"]


@pytest.mark.django_db
def test_exception_handler_unknown_exception() -> None:
    response = hub_exception_handler(RuntimeError("unexpected"), {})
    assert response is not None
    assert response.status_code == 500
    assert response.data == {"ok": False, "error": "internal_server_error"}
