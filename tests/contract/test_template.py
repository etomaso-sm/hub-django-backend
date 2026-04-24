from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
from conftest import assert_matches_fixture


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: dict[str, object]

    def json(self) -> dict[str, object]:
        return self.payload


def write_fixture(path: Path, body: dict[str, object], status: int = 200) -> None:
    path.write_text(
        json.dumps(
            {
                "request": {
                    "method": "GET",
                    "path": "/api/example",
                    "path_pattern": "/api/example",
                },
                "response_status": status,
                "response_headers": {"content-type": "application/json"},
                "response_body": body,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def test_assert_matches_fixture_accepts_matching_response(tmp_path: Path) -> None:
    fixture_path = tmp_path / "example.json"
    write_fixture(fixture_path, {"ok": True, "data": {"name": "alpha"}})

    assert_matches_fixture(
        FakeResponse(200, {"ok": True, "data": {"name": "alpha"}}),
        fixture_path,
        [],
    )


def test_assert_matches_fixture_ignores_declared_volatile_fields(tmp_path: Path) -> None:
    fixture_path = tmp_path / "example.json"
    write_fixture(fixture_path, {"ok": True, "data": {"name": "alpha", "timestamp": "old"}})

    assert_matches_fixture(
        FakeResponse(200, {"ok": True, "data": {"name": "alpha", "timestamp": "new"}}),
        fixture_path,
        ["$.data.timestamp"],
    )


def test_assert_matches_fixture_detects_one_character_diff(tmp_path: Path) -> None:
    fixture_path = tmp_path / "example.json"
    write_fixture(fixture_path, {"ok": True, "data": {"name": "alpha"}})

    with pytest.raises(AssertionError) as excinfo:
        assert_matches_fixture(
            FakeResponse(200, {"ok": True, "data": {"name": "alphb"}}),
            fixture_path,
            [],
        )

    message = str(excinfo.value)
    assert "response body differs from fixture" in message
    assert '-    "name": "alpha"' in message
    assert '+    "name": "alphb"' in message
