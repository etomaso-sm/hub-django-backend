"""Tests for local Caddy routing-table generation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "build_caddyfile.py"


def _load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_caddyfile", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_routes_are_sorted_by_specificity(tmp_path: Path) -> None:
    builder = _load_builder()
    table = tmp_path / "routing-table.json"
    table.write_text("""
        {
          "routes": [
            {"path": "/api/*", "target": "mock"},
            {"path": "/api/reports/*", "target": "django"},
            {"path": "/api/reports/export", "target": "django"}
          ]
        }
        """)

    routes = builder.load_routes(table)

    assert [route["path"] for route in routes] == [
        "/api/reports/export",
        "/api/reports/*",
        "/api/*",
    ]


def test_generated_caddyfile_preserves_sse_and_marks_target() -> None:
    builder = _load_builder()
    rendered = builder.generate_caddyfile(
        [
            {"path": "/api/_smoke/*", "target": "django"},
            {"path": "/api/*", "target": "mock"},
        ]
    )

    assert "@r0 path /api/_smoke/*" in rendered
    assert '@preflight method OPTIONS' in rendered
    assert 'Access-Control-Allow-Origin "http://localhost:5173"' in rendered
    assert 'Access-Control-Allow-Headers "Authorization, Content-Type, X-Xray-Session"' in rendered
    assert "reverse_proxy @r0 django:8000" in rendered
    assert "flush_interval -1" in rendered
    assert "header_up X-Hub-Router django" in rendered
    assert "reverse_proxy @r1 mock-legacy:8787" in rendered
    assert "header_up X-Hub-Router mock" in rendered


def test_wildcard_is_only_supported_as_suffix(tmp_path: Path) -> None:
    builder = _load_builder()
    table = tmp_path / "routing-table.json"
    table.write_text('{"routes": [{"path": "/api/*/bad", "target": "mock"}]}')

    with pytest.raises(ValueError, match="wildcard is only supported as a suffix"):
        builder.load_routes(table)


def test_unknown_target_fails_loudly(tmp_path: Path) -> None:
    builder = _load_builder()
    table = tmp_path / "routing-table.json"
    table.write_text('{"routes": [{"path": "/api/*", "target": "legacy"}]}')

    with pytest.raises(ValueError, match="unknown target 'legacy'"):
        builder.load_routes(table)
