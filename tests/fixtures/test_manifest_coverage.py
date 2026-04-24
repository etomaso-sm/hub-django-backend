from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools.capture_fixtures import Route, load_manifest

FIXTURE_ROOT = Path(__file__).resolve().parent
MANIFEST = Path(__file__).resolve().parents[2] / "tools/route_manifest.yaml"


def fixture_path(route: Route) -> Path:
    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", route.name).strip("_")
    return FIXTURE_ROOT / route.app / f"{safe_name}.json"


def load_fixture(route: Route) -> dict[str, Any]:
    path = fixture_path(route)
    assert path.exists(), f"missing fixture for {route.method} {route.path}: {path}"
    return json.loads(path.read_text())


def test_fixture_exists_for_every_manifest_route() -> None:
    routes = load_manifest(MANIFEST)

    missing = [str(fixture_path(route)) for route in routes if not fixture_path(route).exists()]

    assert missing == []


def test_fixtures_match_manifest_requests() -> None:
    for route in load_manifest(MANIFEST):
        fixture = load_fixture(route)
        request = fixture["request"]

        assert request["method"] == route.method
        assert request["path"] == route.path
        assert request["path_pattern"] == route.path_pattern
        assert isinstance(fixture["response_status"], int)
        assert isinstance(fixture["response_headers"], dict)
        if route.sse:
            assert "response_events" in fixture
            assert isinstance(fixture["response_events"], list)
        else:
            assert "response_body" in fixture
