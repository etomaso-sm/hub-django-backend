"""Hub auth models.

Minimal scaffold for TKT-005. The `People` table is *global* (not per-tenant)
because a single person can belong to multiple hubs. Tenant membership lives
in `user_tenants` (modelled in a later ticket).

Later tickets (TKT-008 auth backend, TKT-020 inspectdb model split) expand
this with `hub_session`, `user_tenants`, and the rest of the auth surface the
legacy worker owns under `routes/core.js`.
"""

from django.db import models


class People(models.Model):  # type: ignore[misc]  # django.db.models is untyped
    ROLE_NORMAL = "normal"
    ROLE_STAFF = "staff"
    ROLE_SUPERADMIN = "superadmin"
    ROLE_CHOICES: list[tuple[str, str]] = [
        (ROLE_NORMAL, "normal"),
        (ROLE_STAFF, "staff"),
        (ROLE_SUPERADMIN, "superadmin"),
    ]

    # normal = default user
    # staff = Django-admin viewer
    # superadmin = impersonation + destructive admin
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=200, blank=True, default="")
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_NORMAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "people"
        verbose_name_plural = "People"

    def __str__(self) -> str:
        return str(self.email)

    @property
    def is_staff_role(self) -> bool:
        return bool(self.role in (self.ROLE_STAFF, self.ROLE_SUPERADMIN))

    @property
    def is_superadmin(self) -> bool:
        return bool(self.role == self.ROLE_SUPERADMIN)
