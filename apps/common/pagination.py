"""Hub pagination - honors ?limit=N only, emits {"items": [...]}.

The frontend uses `?limit=N` exclusively (no cursor, offset, or page). It uses
`len(items) >= limit` as a "more available" heuristic, so we deliberately do
not emit `count`, `next`, or `previous` — keeps responses small and matches
the current worker's shape.

Clamp rules (from TKT-003):
- limit <= 0       -> 1
- limit > 500      -> 500 (max_limit)
- limit invalid    -> 50 (default_limit)
- limit unset      -> 50 (default_limit)
"""

from typing import Any

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response


class HubLimitPagination(LimitOffsetPagination):  # type: ignore[misc]  # DRF class is untyped
    default_limit = 50
    max_limit = 500
    limit_query_param = "limit"
    # We do not document offset because the frontend never sends it, but DRF's
    # base class still reads it; leaving the default ("offset") keeps compat
    # for any accidental callers without exposing a new surface.

    def get_limit(self, request: Request) -> int:
        raw = request.query_params.get(self.limit_query_param)
        if raw is None:
            return self.default_limit
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return self.default_limit
        if value < 1:
            return 1
        if value > self.max_limit:
            return self.max_limit
        return value

    def get_paginated_response(self, data: Any) -> Response:
        return Response({"items": data})
