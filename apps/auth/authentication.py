"""HubAuthentication - DRF BaseAuthentication with CF Access + session + service token.

Resolution order on every protected request:

1. **DEV_BYPASS_AUTH_AS_EMAIL** (DEBUG only) — if set, resolve that email to
   a People row and skip the rest. Lets local Playwright scenarios run
   without a real CF Access frontend.
2. **CF Access** — either the ``CF-Access-Jwt-Assertion`` header (verified
   against JWKS) OR the ``Cf-Access-Authenticated-User-Email`` header. JWT
   wins if both are present.
3. **hub_session cookie** — token lookup in the ``sessions`` table, expiry
   enforced.
4. **Service token** — ``Authorization: Bearer <token>`` matched against
   ``settings.SERVICE_TOKENS`` (a dict of ``{token: email}``).

When none match, returns ``None`` so DRF continues to the permission chain
(which decides 401 vs public).

Explicit failures (invalid JWT, expired session, unknown email) raise
``AuthenticationFailed`` so DRF returns a 401 with the envelope.
"""

from typing import Any, cast

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.auth.models import People, Session
from apps.common.jwks import verify_cf_access_jwt


class HubAuthentication(BaseAuthentication):  # type: ignore[misc]  # DRF untyped
    def authenticate(self, request: Any) -> tuple[People, None] | None:
        # 1. Dev bypass (DEBUG only).
        bypass_email = getattr(settings, "DEV_BYPASS_AUTH_AS_EMAIL", None)
        if settings.DEBUG and bypass_email:
            return self._resolve_or_fail(bypass_email), None

        # 2. CF Access — JWT preferred, email header accepted as fallback.
        user = self._try_cf_access(request)
        if user is not None:
            return user, None

        # 3. hub_session cookie.
        user = self._try_hub_session(request)
        if user is not None:
            return user, None

        # 4. Service token.
        user = self._try_service_token(request)
        if user is not None:
            return user, None

        # None matched: let permissions handle 401/403.
        return None

    # ---------- individual paths ----------

    def _try_cf_access(self, request: Any) -> People | None:
        jwt_token = request.META.get("HTTP_CF_ACCESS_JWT_ASSERTION")
        email_header = request.META.get("HTTP_CF_ACCESS_AUTHENTICATED_USER_EMAIL")

        if not jwt_token and not email_header:
            return None

        email: str | None = None

        if jwt_token:
            jwks_url = getattr(settings, "CF_ACCESS_JWKS_URL", None)
            audience = getattr(settings, "CF_ACCESS_AUD", None)
            if not jwks_url or not audience:
                # Misconfigured origin — treat as auth failure, not silent pass.
                raise AuthenticationFailed("cf_access_not_configured")
            try:
                claims = verify_cf_access_jwt(jwt_token, jwks_url=jwks_url, audience=audience)
            except jwt.InvalidTokenError as exc:
                raise AuthenticationFailed(f"cf_access_jwt_invalid: {exc}") from exc
            email = claims.get("email") or claims.get("identity_nonce")

        if not email and email_header:
            email = email_header

        if not email:
            raise AuthenticationFailed("cf_access_no_email")

        return self._resolve_or_fail(email)

    def _try_hub_session(self, request: Any) -> People | None:
        cookie_name = getattr(settings, "SESSION_COOKIE_NAME", "hub_session")
        token = request.COOKIES.get(cookie_name)
        if not token:
            return None
        try:
            session = Session.objects.select_related("person").get(token=token)
        except Session.DoesNotExist as exc:
            raise AuthenticationFailed("session_invalid") from exc
        if session.expires_at < timezone.now():
            raise AuthenticationFailed("session_expired")
        return session.person  # type: ignore[no-any-return]

    def _try_service_token(self, request: Any) -> People | None:
        header = request.META.get("HTTP_AUTHORIZATION", "")
        if not header.startswith("Bearer "):
            return None
        raw = header[len("Bearer ") :].strip()
        if not raw:
            return None
        known: dict[str, str] = getattr(settings, "SERVICE_TOKENS", {}) or {}
        email = known.get(raw)
        if not email:
            raise AuthenticationFailed("service_token_invalid")
        return self._resolve_or_fail(email)

    @staticmethod
    def _resolve_or_fail(email: str) -> People:
        try:
            return cast(People, People.objects.get(email=email))
        except People.DoesNotExist as exc:
            raise AuthenticationFailed(f"unknown_user: {email}") from exc
