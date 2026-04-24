from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast

import pytest
from django.core.management import call_command

from apps.auth.models import People, Session
from tools.capture_seed import sanitize_seed

SEED_PATH = Path("fixtures/seed_hub_sprint_mode.json")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<![\w])(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?![\w])")
BLOCKED_NAMES = {"aaron", "eugenio", "hugh", "clayton", "dani"}


def _all_strings(value: Any) -> list[str]:
    if isinstance(value, dict):
        out: list[str] = []
        for item in value.values():
            out.extend(_all_strings(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(_all_strings(item))
        return out
    return [value] if isinstance(value, str) else []


def test_sanitizer_replaces_source_pii_deterministically() -> None:
    source = [
        {
            "model": "hub_auth.people",
            "pk": 10,
            "fields": {
                "email": "real.person@example.com",
                "display_name": "Real Person",
                "note": "Call +1 415-555-1212; ssn 123-45-6789",
            },
        }
    ]

    sanitized = sanitize_seed(source)

    fields = sanitized[0]["fields"]
    assert fields["email"] == "user001@example.test"
    assert fields["display_name"] == "Example User 001"
    assert fields["note"] == "Call <redacted-phone>; ssn <redacted-ssn>"


def test_seed_contains_no_real_pii_patterns() -> None:
    strings = _all_strings(json.loads(SEED_PATH.read_text()))

    for value in strings:
        for match in EMAIL_RE.finditer(value):
            assert match.group(1).lower() in {"local.test", "example.test"}
        assert PHONE_RE.search(value) is None
        lowered = value.lower()
        assert not any(name in lowered for name in BLOCKED_NAMES)


@pytest.mark.django_db
def test_seed_loads_and_creates_required_users() -> None:
    call_command("loaddata", str(SEED_PATH), verbosity=0)

    roles = cast(dict[str, str], dict(People.objects.values_list("email", "role")))
    assert roles["normal@local.test"] == "normal"
    assert roles["staff@local.test"] == "staff"
    assert roles["super@local.test"] == "superadmin"
    assert Session.objects.filter(
        pk="dev-session-normal", person__email="normal@local.test"
    ).exists()
