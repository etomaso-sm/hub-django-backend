#!/usr/bin/env python3
"""Create a sanitized Django seed fixture for the local migration stack."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.capture_fixtures import scrub_pii  # noqa: E402

NAME_KEYS = {"display_name", "full_name", "first_name", "last_name", "name"}
EMAIL_KEYS = {"email", "user_email"}


class DeterministicSanitizer:
    def __init__(self) -> None:
        self._email_map: dict[str, str] = {}
        self._name_map: dict[str, str] = {}

    def email(self, value: str) -> str:
        if value not in self._email_map:
            self._email_map[value] = f"user{len(self._email_map) + 1:03d}@example.test"
        return self._email_map[value]

    def name(self, value: str) -> str:
        if value not in self._name_map:
            self._name_map[value] = f"Example User {len(self._name_map) + 1:03d}"
        return self._name_map[value]

    def sanitize(self, value: Any, key: str | None = None) -> Any:
        if isinstance(value, dict):
            return {
                item_key: self.sanitize(item_value, item_key)
                for item_key, item_value in value.items()
            }
        if isinstance(value, list):
            return [self.sanitize(item) for item in value]
        if isinstance(value, str):
            if key in EMAIL_KEYS and "@" in value:
                return self.email(value)
            if key in NAME_KEYS and value and not value.endswith(".test"):
                return self.name(value)
            return scrub_pii(value)
        return value


def build_default_seed() -> list[dict[str, Any]]:
    return [
        {
            "model": "hub_auth.people",
            "pk": 1,
            "fields": {
                "email": "normal@local.test",
                "display_name": "Normal User",
                "role": "normal",
                "created_at": "2026-04-24T00:00:00Z",
            },
        },
        {
            "model": "hub_auth.people",
            "pk": 2,
            "fields": {
                "email": "staff@local.test",
                "display_name": "Staff User",
                "role": "staff",
                "created_at": "2026-04-24T00:00:00Z",
            },
        },
        {
            "model": "hub_auth.people",
            "pk": 3,
            "fields": {
                "email": "super@local.test",
                "display_name": "Super Admin",
                "role": "superadmin",
                "created_at": "2026-04-24T00:00:00Z",
            },
        },
        {
            "model": "hub_auth.session",
            "pk": "dev-session-normal",
            "fields": {
                "person": 1,
                "expires_at": "2027-04-24T00:00:00Z",
                "created_at": "2026-04-24T00:00:00Z",
            },
        },
    ]


def sanitize_seed(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sanitizer = DeterministicSanitizer()
    return cast(list[dict[str, Any]], sanitizer.sanitize(records))


def write_seed(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-json", type=Path)
    parser.add_argument("--output", type=Path, default=Path("fixtures/seed_hub_sprint_mode.json"))
    args = parser.parse_args(argv)

    try:
        if args.source_json:
            records = json.loads(args.source_json.read_text())
            if not isinstance(records, list):
                raise ValueError("source JSON must be a list of Django fixture records")
            output = sanitize_seed(records)
        else:
            output = build_default_seed()
        write_seed(output, args.output)
    except Exception as exc:  # noqa: BLE001 - CLI should report cleanly.
        print(f"capture seed failed: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
