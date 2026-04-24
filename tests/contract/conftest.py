from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Any

from tools.capture_fixtures import strip_volatile_fields


def _response_status(response: Any) -> int | None:
    status = getattr(response, "status_code", None)
    if status is None:
        status = getattr(response, "status", None)
    return int(status) if status is not None else None


def _response_body(response: Any) -> Any:
    if isinstance(response, dict | list | str | int | float | bool) or response is None:
        return response

    json_method = getattr(response, "json", None)
    if callable(json_method):
        return json_method()

    content = getattr(response, "content", None)
    if content is None:
        content = getattr(response, "text", None)
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    if isinstance(content, str):
        return json.loads(content)

    data = getattr(response, "data", None)
    if data is not None:
        return data

    raise TypeError(f"unsupported response type: {type(response)!r}")


def _stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _unified_diff(expected: Any, actual: Any) -> str:
    return "".join(
        difflib.unified_diff(
            _stable_json(expected).splitlines(keepends=True),
            _stable_json(actual).splitlines(keepends=True),
            fromfile="fixture",
            tofile="response",
        )
    )


def assert_matches_fixture(
    response: Any,
    fixture_path: str | Path,
    volatile_fields: list[str] | None = None,
) -> None:
    fixture = json.loads(Path(fixture_path).read_text())
    expected_status = int(fixture["response_status"])
    actual_status = _response_status(response)
    if actual_status is not None and actual_status != expected_status:
        raise AssertionError(f"status mismatch: expected {expected_status}, got {actual_status}")

    if "response_events" in fixture:
        raise AssertionError("SSE event sequence diffing is covered by TKT-050")

    fields = volatile_fields or []
    expected = strip_volatile_fields(fixture["response_body"], fields)
    actual = strip_volatile_fields(_response_body(response), fields)
    if actual != expected:
        diff = _unified_diff(expected, actual)
        raise AssertionError(f"response body differs from fixture:\n{diff}")
