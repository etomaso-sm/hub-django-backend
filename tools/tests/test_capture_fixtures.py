from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from tools.capture_fixtures import (
    Route,
    capture_routes,
    load_manifest,
    scrub_pii,
    strip_volatile_fields,
)


class CaptureHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/api/__capture/events"):
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b"event: status\n")
            self.wfile.write(b'data: {"email":"alice@example.com"}\n\n')
            self.wfile.write(b"event: done\n")
            self.wfile.write(b"data: [DONE]\n\n")
            return

        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("x-fixture", "capture")
        self.end_headers()
        payload = {
            "ok": True,
            "data": {
                "path": self.path.split("?", 1)[0],
                "email": "alice@example.com",
                "phone": "(415) 555-1212",
                "ssn": "123-45-6789",
                "timestamp": "2026-04-24T00:00:00Z",
            },
        }
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def log_message(self, *_args: Any) -> None:
        return


def serve() -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), CaptureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}"


def test_scrub_pii_recursively() -> None:
    scrubbed = scrub_pii(
        {
            "email": "alice@example.com",
            "nested": ["call +1 415-555-1212", "ssn 123-45-6789"],
        }
    )

    assert scrubbed == {
        "email": "<redacted-email>",
        "nested": ["call <redacted-phone>", "ssn <redacted-ssn>"],
    }


def test_strip_volatile_fields_removes_json_paths() -> None:
    payload = {"ok": True, "data": {"timestamp": "now", "stable": "keep"}}

    assert strip_volatile_fields(payload, ["$.data.timestamp"]) == {
        "ok": True,
        "data": {"stable": "keep"},
    }


def test_load_manifest_reads_safe_sse_route(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("""
routes:
  - app: stream
    name: events
    method: GET
    path: /api/events
    safe: true
    sse: true
""")

    routes = load_manifest(manifest)

    assert routes == [
        Route(
            app="stream",
            name="events",
            method="GET",
            path="/api/events",
            path_pattern="/api/events",
            safe=True,
            sse=True,
        )
    ]


def test_capture_against_throwaway_server_writes_ten_safe_fixtures(tmp_path: Path) -> None:
    server, base_url = serve()
    routes = [
        Route(
            app="safe",
            name=f"route_{idx}",
            method="GET",
            path=f"/api/__capture/safe-{idx}",
            path_pattern=f"/api/__capture/safe-{idx}",
            safe=True,
        )
        for idx in range(10)
    ]
    try:
        written = capture_routes(
            routes,
            base_url=base_url,
            output_root=tmp_path,
            tenant="throwaway",
            only_safe=True,
            limit=10,
            volatile_fields={routes[0].path: ["$.data.timestamp"]},
            sse_max_events=5,
            timeout=2.0,
        )
    finally:
        server.shutdown()

    assert len(written) == 10
    captured = json.loads((tmp_path / "safe/route_0.json").read_text())
    assert captured["response_status"] == 200
    assert captured["response_headers"]["x-fixture"] == "capture"
    assert captured["response_body"]["data"]["email"] == "<redacted-email>"
    assert captured["response_body"]["data"]["phone"] == "<redacted-phone>"
    assert captured["response_body"]["data"]["ssn"] == "<redacted-ssn>"
    assert "timestamp" not in captured["response_body"]["data"]


def test_capture_sse_records_event_stream(tmp_path: Path) -> None:
    server, base_url = serve()
    route = Route(
        app="stream",
        name="events",
        method="GET",
        path="/api/__capture/events",
        path_pattern="/api/__capture/events",
        safe=True,
        sse=True,
    )
    try:
        capture_routes(
            [route],
            base_url=base_url,
            output_root=tmp_path,
            tenant="throwaway",
            only_safe=True,
            limit=1,
            volatile_fields={},
            sse_max_events=2,
            timeout=2.0,
        )
    finally:
        server.shutdown()

    captured = json.loads((tmp_path / "stream/events.json").read_text())
    assert captured["response_events"][0]["event"] == "status"
    assert captured["response_events"][0]["data"]["email"] == "<redacted-email>"
    assert isinstance(captured["response_events"][0]["ts_offset_ms"], int)
    assert captured["response_events"][1]["data"] == "[DONE]"
