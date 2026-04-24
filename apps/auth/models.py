"""Hub auth models.

The `People` table is *global* (not per-tenant) because a single person can
belong to multiple hubs. `Session` stores hub_session cookie tokens issued
to People on login.

TKT-020 (inspectdb split) will eventually replace these with the full set of
models from the legacy schema (user_tenants, etc.).
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
    def is_authenticated(self) -> bool:
        """Django / DRF treat any truthy user as authenticated; mirror that."""
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_staff_role(self) -> bool:
        return bool(self.role in (self.ROLE_STAFF, self.ROLE_SUPERADMIN))

    @property
    def is_superadmin(self) -> bool:
        return bool(self.role == self.ROLE_SUPERADMIN)


class Session(models.Model):  # type: ignore[misc]  # django.db.models is untyped
    """Hub session token → People mapping.

    Cookie name is ``SESSION_COOKIE_NAME`` (``hub_session``). Expiry is
    enforced in ``HubAuthentication`` by comparing ``expires_at`` to now.

    This is intentionally separate from ``django.contrib.sessions`` because
    the legacy worker owns its own session lifetime and hash format.
    """

    token = models.CharField(max_length=200, primary_key=True)
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name="sessions")
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sessions"

    def __str__(self) -> str:
        return f"Session({self.person_id}, {self.token[:8]}...)"
