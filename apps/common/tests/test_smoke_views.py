from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest
from django.core.management import call_command
from django.test import override_settings
from rest_framework.test import APIClient

SEED_PATH = Path("fixtures/seed_hub_sprint_mode.json")


@pytest.mark.django_db
def test_smoke_ping_is_authenticated_and_enveloped() -> None:
    with override_settings(DEBUG=True, DEV_BYPASS_AUTH_AS_EMAIL="normal@local.test"):
        call_command("loaddata", str(SEED_PATH), verbosity=0)

        response = APIClient().get("/api/_smoke/ping")

    assert response.status_code == 200
    body = cast(dict[str, Any], response.json())
    assert body == {
        "ok": True,
        "data": {
            "pong": True,
            "user_email": "normal@local.test",
        },
    }
