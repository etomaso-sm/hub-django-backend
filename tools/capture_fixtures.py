#!/usr/bin/env python3
"""Capture legacy worker responses into deterministic fixture files.

The real run points --base-url at the current worker and supplies credentials
through environment variables. Tests use a local throwaway server, so verify
never depends on the internet or secrets.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<![\w])(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?![\w])")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

VOLATILE_RESPONSE_HEADERS = {
    "connection",
    "content-encoding",
    "content-length",
    "date",
    "server",
    "transfer-encoding",
}


@dataclass(frozen=True)
class Route:
    app: str
    name: str
    method: str
    path: str
    path_pattern: str
    safe: bool
    sse: bool = False


def _parse_scalar(value: str) -> str | bool | int:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _parse_simple_yaml_mapping(path: Path) -> dict[str, Any]:
    """Parse the tiny YAML subset used by route_manifest.yaml.

    Supported:
    - top-level `routes:` list of flat mappings
    - top-level string keys whose value is a list of strings
    """

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_item: dict[str, Any] | None = None

    for raw_line in path.read_text().splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        if not line.startswith(" "):
            key, _, raw_value = line.partition(":")
            key = key.strip().strip("\"'")
            if raw_value.strip():
                result[key] = _parse_scalar(raw_value)
                current_list_key = None
            else:
                result[key] = []
                current_list_key = key
            current_item = None
            continue

        stripped = line.strip()
        if stripped.startswith("- "):
            value = stripped[2:]
            if ":" in value:
                key, _, raw_value = value.partition(":")
                current_item = {key.strip(): _parse_scalar(raw_value)}
                result.setdefault(current_list_key or "", []).append(current_item)
            else:
                result.setdefault(current_list_key or "", []).append(_parse_scalar(value))
                current_item = None
            continue

        if current_item is None or ":" not in stripped:
            raise ValueError(f"unsupported yaml line in {path}: {raw_line}")
        key, _, raw_value = stripped.partition(":")
        current_item[key.strip()] = _parse_scalar(raw_value)

    return result


def load_manifest(path: Path) -> list[Route]:
    data = _parse_simple_yaml_mapping(path)
    raw_routes = data.get("routes", [])
    if not isinstance(raw_routes, list):
        raise ValueError("route manifest must contain a routes list")

    routes: list[Route] = []
    for idx, raw_route in enumerate(raw_routes):
        if not isinstance(raw_route, dict):
            raise ValueError(f"route #{idx} must be a mapping")
        app = str(raw_route.get("app") or "").strip()
        name = str(raw_route.get("name") or "").strip()
        method = str(raw_route.get("method") or "GET").upper()
        route_path = str(raw_route.get("path") or "").strip()
        path_pattern = str(raw_route.get("path_pattern") or route_path).strip()
        safe = bool(raw_route.get("safe", False))
        sse = bool(raw_route.get("sse", False))
        if not app or not name or not route_path.startswith("/"):
            raise ValueError(f"route #{idx} is missing app, name, or absolute path")
        routes.append(
            Route(
                app=app,
                name=name,
                method=method,
                path=route_path,
                path_pattern=path_pattern,
                safe=safe,
                sse=sse,
            )
        )
    return routes


def load_volatile_fields(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    data = _parse_simple_yaml_mapping(path)
    out: dict[str, list[str]] = {}
    for key, value in data.items():
        if isinstance(value, list):
            out[key] = [str(item) for item in value]
    return out


def scrub_pii(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: scrub_pii(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub_pii(item) for item in value]
    if isinstance(value, str):
        value = EMAIL_RE.sub("<redacted-email>", value)
        value = PHONE_RE.sub("<redacted-phone>", value)
        value = SSN_RE.sub("<redacted-ssn>", value)
        return value
    return value


def _remove_json_path(payload: Any, json_path: str) -> None:
    if not json_path.startswith("$."):
        return
    parts = json_path[2:].split(".")
    current = payload
    for part in parts[:-1]:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return
    if isinstance(current, dict):
        current.pop(parts[-1], None)


def strip_volatile_fields(payload: Any, fields: list[str]) -> Any:
    stripped = copy.deepcopy(payload)
    for field in fields:
        _remove_json_path(stripped, field)
    return stripped


def _fixture_filename(route: Route) -> Path:
    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", route.name).strip("_")
    return Path(route.app) / f"{safe_name}.json"


def build_headers() -> dict[str, str]:
    headers = {"accept": "application/json, text/event-stream;q=0.9, */*;q=0.1"}
    if os.environ.get("CAPTURE_COOKIE"):
        headers["cookie"] = os.environ["CAPTURE_COOKIE"]
    if os.environ.get("CAPTURE_BEARER_TOKEN"):
        headers["authorization"] = f"Bearer {os.environ['CAPTURE_BEARER_TOKEN']}"
    if os.environ.get("CAPTURE_AUTH_HEADER"):
        name, _, value = os.environ["CAPTURE_AUTH_HEADER"].partition(":")
        if name.strip() and value.strip():
            headers[name.strip()] = value.strip()
    return headers


def _route_url(base_url: str, route: Route, tenant: str | None) -> str:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", route.path.lstrip("/"))
    if tenant:
        parsed = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        query.append(("tenant", tenant))
        url = urllib.parse.urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                urllib.parse.urlencode(query),
                parsed.fragment,
            )
        )
    return url


def _response_headers(response: Any) -> dict[str, str]:
    headers: dict[str, str] = {}
    for key, value in response.headers.items():
        if key.lower() not in VOLATILE_RESPONSE_HEADERS:
            headers[key.lower()] = value
    return headers


def _decode_json_or_text(raw_body: bytes, content_type: str) -> Any:
    text = raw_body.decode("utf-8", errors="replace")
    if "application/json" in content_type:
        return json.loads(text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _parse_sse_block(block: list[str], started: float) -> dict[str, Any] | None:
    if not block:
        return None
    event: dict[str, Any] = {"event": "message", "data": ""}
    data_lines = []
    for line in block:
        field, _, value = line.partition(":")
        value = value[1:] if value.startswith(" ") else value
        if field == "event":
            event["event"] = value
        elif field == "data":
            data_lines.append(value)
        elif field == "id":
            event["id"] = value
        elif field == "retry":
            event["retry"] = value
    data = "\n".join(data_lines)
    try:
        event["data"] = json.loads(data)
    except json.JSONDecodeError:
        event["data"] = data
    event["ts_offset_ms"] = int((time.monotonic() - started) * 1000)
    return event


def _read_sse_events(response: Any, max_events: int) -> list[dict[str, Any]]:
    started = time.monotonic()
    events: list[dict[str, Any]] = []
    block: list[str] = []
    while len(events) < max_events:
        raw_line = response.readline()
        if not raw_line:
            break
        line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
        if line == "":
            parsed = _parse_sse_block(block, started)
            if parsed is not None:
                events.append(parsed)
            block = []
        else:
            block.append(line)
    return events


def capture_route(
    base_url: str,
    route: Route,
    *,
    tenant: str | None,
    headers: dict[str, str],
    volatile_fields: dict[str, list[str]],
    sse_max_events: int,
    timeout: float,
) -> dict[str, Any]:
    url = _route_url(base_url, route, tenant)
    request = urllib.request.Request(url=url, method=route.method, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=timeout)  # noqa: S310
    except urllib.error.HTTPError as error:
        response = error

    fixture: dict[str, Any] = {
        "request": {
            "method": route.method,
            "path": route.path,
            "path_pattern": route.path_pattern,
            "tenant": tenant,
        },
        "response_status": response.status,
        "response_headers": _response_headers(response),
    }

    if route.sse:
        fixture["response_events"] = scrub_pii(_read_sse_events(response, sse_max_events))
        return fixture

    raw_body = response.read()
    body = _decode_json_or_text(raw_body, response.headers.get("content-type", ""))
    body = scrub_pii(strip_volatile_fields(body, volatile_fields.get(route.path, [])))
    fixture["response_body"] = body
    return fixture


def capture_routes(
    routes: list[Route],
    *,
    base_url: str,
    output_root: Path,
    tenant: str | None,
    only_safe: bool,
    limit: int | None,
    volatile_fields: dict[str, list[str]],
    sse_max_events: int,
    timeout: float,
) -> list[Path]:
    selected = [route for route in routes if route.safe or not only_safe]
    if limit is not None:
        selected = selected[:limit]

    headers = build_headers()
    written: list[Path] = []
    for route in selected:
        fixture = capture_route(
            base_url,
            route,
            tenant=tenant,
            headers=headers,
            volatile_fields=volatile_fields,
            sse_max_events=sse_max_events,
            timeout=timeout,
        )
        fixture_path = output_root / _fixture_filename(route)
        fixture_path.parent.mkdir(parents=True, exist_ok=True)
        fixture_path.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n")
        written.append(fixture_path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=os.environ.get("CAPTURE_BASE_URL"))
    parser.add_argument("--manifest", type=Path, default=Path("tools/route_manifest.yaml"))
    parser.add_argument("--volatile-fields", type=Path, default=Path("tools/volatile_fields.yaml"))
    parser.add_argument("--output-root", type=Path, default=Path("tests/fixtures"))
    parser.add_argument("--tenant", default=os.environ.get("CAPTURE_TENANT", "throwaway"))
    parser.add_argument("--only-safe", action="store_true", default=True)
    parser.add_argument("--include-unsafe", action="store_false", dest="only_safe")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sse-max-events", type=int, default=25)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args(argv)

    if not args.base_url:
        print("CAPTURE_BASE_URL or --base-url is required", file=sys.stderr)
        return 2

    try:
        routes = load_manifest(args.manifest)
        volatile_fields = load_volatile_fields(args.volatile_fields)
        written = capture_routes(
            routes,
            base_url=args.base_url,
            output_root=args.output_root,
            tenant=args.tenant,
            only_safe=args.only_safe,
            limit=args.limit,
            volatile_fields=volatile_fields,
            sse_max_events=args.sse_max_events,
            timeout=args.timeout,
        )
    except Exception as exc:  # noqa: BLE001 - command-line tool reports cleanly.
        print(f"capture failed: {exc}", file=sys.stderr)
        return 1

    print(f"captured {len(written)} fixture(s)")
    for path_written in written:
        print(path_written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
