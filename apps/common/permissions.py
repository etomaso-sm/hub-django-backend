"""DRF permission classes for the hub.

Three classes:

- ``IsAuthenticatedOrPublic`` — default class, enforced globally. Allows
  any request whose path matches a pattern in ``settings.PUBLIC_URL_PATTERNS``
  (webhooks, health, signup, etc.); otherwise requires an authenticated user.
  Patterns use fnmatch-style globs (``?``, ``*``, ``[abc]``).
- ``IsStaff`` — authenticated + role in {staff, superadmin}.
- ``IsSuperadmin`` — authenticated + role == superadmin.

Role ladder: normal < staff < superadmin.
"""

import fnmatch
from typing import Any

from django.conf import settings
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthenticatedOrPublic(BasePermission):  # type: ignore[misc]  # DRF untyped
    """Default global permission. Public patterns skip auth; everything else requires it."""

    def has_permission(self, request: Any, view: Any) -> bool:
        patterns: list[str] = getattr(settings, "PUBLIC_URL_PATTERNS", [])
        path = request.path
        for pattern in patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        user = getattr(request, "user", None)
        return bool(user is not None and getattr(user, "is_authenticated", False))


class IsStaff(IsAuthenticated):  # type: ignore[misc]  # DRF untyped
    """Authenticated user whose role is staff or superadmin."""

    def has_permission(self, request: Any, view: Any) -> bool:
        if not super().has_permission(request, view):
            return False
        return getattr(request.user, "role", None) in ("staff", "superadmin")


class IsSuperadmin(IsAuthenticated):  # type: ignore[misc]  # DRF untyped
    """Authenticated user whose role is exactly superadmin."""

    def has_permission(self, request: Any, view: Any) -> bool:
        if not super().has_permission(request, view):
            return False
        return getattr(request.user, "role", None) == "superadmin"
