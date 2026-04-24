"""DRF permission classes keyed on the hub `role` field.

These permissions defer to `IsAuthenticated` first, then check the role on
`request.user`. The actual user resolution (CF Access JWT, hub_session
cookie, etc.) lands in TKT-008; these permission classes work with any user
object that exposes a string `role` attribute.

Role ladder (lowest -> highest):
  normal < staff < superadmin

- ``IsStaff`` allows staff and superadmin.
- ``IsSuperadmin`` allows superadmin only (used for impersonation, raw SQL,
  destructive admin actions).
"""

from typing import Any

from rest_framework.permissions import IsAuthenticated


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
