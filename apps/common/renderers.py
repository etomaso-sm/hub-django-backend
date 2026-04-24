"""Hub JSON renderer - wraps success responses as {"ok": true, "data": ...}."""

from typing import Any, cast

from rest_framework.renderers import JSONRenderer


class HubJSONRenderer(JSONRenderer):  # type: ignore[misc]  # DRF JSONRenderer is untyped
    """Wrap success responses as ``{"ok": true, "data": <payload>}``.

    Views can opt out of the wrap by setting ``raw_response = True`` as a
    class attribute, or by decorating a function-based view with
    ``apps.common.exceptions.raw_response``. Opt-out is intended for webhook
    endpoints (Stripe, privacy, etc.) that must emit unwrapped JSON.

    Error responses are produced by ``hub_exception_handler`` (pre-wrapped);
    this renderer detects the envelope shape and passes it through unchanged.
    """

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict[str, Any] | None = None,
    ) -> bytes:
        if data is None:
            return b""

        if _is_already_wrapped(data):
            return cast(bytes, super().render(data, accepted_media_type, renderer_context))

        if renderer_context is not None and _is_raw_response(renderer_context):
            return cast(bytes, super().render(data, accepted_media_type, renderer_context))

        wrapped = {"ok": True, "data": data}
        return cast(bytes, super().render(wrapped, accepted_media_type, renderer_context))


def _is_already_wrapped(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    keys = set(data.keys())
    return keys == {"ok", "data"} or keys == {"ok", "error"}


def _is_raw_response(renderer_context: dict[str, Any]) -> bool:
    view = renderer_context.get("view")
    if view is not None and getattr(view, "raw_response", False):
        return True

    request = renderer_context.get("request")
    if request is not None:
        resolver = getattr(request, "resolver_match", None)
        if resolver is not None:
            func = resolver.func
            if getattr(func, "_raw_response", False):
                return True
            cls = getattr(func, "cls", None)
            if cls is not None and getattr(cls, "_raw_response", False):
                return True
    return False
