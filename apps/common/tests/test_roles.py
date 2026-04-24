"""Tests for IsStaff / IsSuperadmin permission classes."""

from types import SimpleNamespace

from apps.common.permissions import IsStaff, IsSuperadmin


def _req(*, authenticated: bool, role: str | None) -> SimpleNamespace:
    """Build a minimal mock request with ``user.is_authenticated`` and ``user.role``."""
    user = SimpleNamespace(is_authenticated=authenticated, role=role)
    return SimpleNamespace(user=user)


# ---------- IsStaff ----------


def test_is_staff_allows_staff() -> None:
    assert IsStaff().has_permission(_req(authenticated=True, role="staff"), None) is True


def test_is_staff_allows_superadmin() -> None:
    assert IsStaff().has_permission(_req(authenticated=True, role="superadmin"), None) is True


def test_is_staff_denies_normal() -> None:
    assert IsStaff().has_permission(_req(authenticated=True, role="normal"), None) is False


def test_is_staff_denies_unauthenticated() -> None:
    assert IsStaff().has_permission(_req(authenticated=False, role="staff"), None) is False


def test_is_staff_denies_missing_role() -> None:
    user = SimpleNamespace(is_authenticated=True)  # no `role` attr at all
    req = SimpleNamespace(user=user)
    assert IsStaff().has_permission(req, None) is False


# ---------- IsSuperadmin ----------


def test_is_superadmin_allows_superadmin() -> None:
    assert IsSuperadmin().has_permission(_req(authenticated=True, role="superadmin"), None) is True


def test_is_superadmin_denies_staff() -> None:
    assert IsSuperadmin().has_permission(_req(authenticated=True, role="staff"), None) is False


def test_is_superadmin_denies_normal() -> None:
    assert IsSuperadmin().has_permission(_req(authenticated=True, role="normal"), None) is False


def test_is_superadmin_denies_unauthenticated() -> None:
    assert (
        IsSuperadmin().has_permission(_req(authenticated=False, role="superadmin"), None) is False
    )


def test_is_superadmin_denies_missing_role() -> None:
    user = SimpleNamespace(is_authenticated=True)
    req = SimpleNamespace(user=user)
    assert IsSuperadmin().has_permission(req, None) is False
