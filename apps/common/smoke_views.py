"""Small authenticated smoke endpoints for local migration tickets."""

from typing import Any

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])  # type: ignore[untyped-decorator]
def ping(request: Any) -> Response:
    """Return a minimal authenticated response through the normal DRF envelope."""
    return Response(
        {
            "pong": True,
            "user_email": request.user.email,
        }
    )
