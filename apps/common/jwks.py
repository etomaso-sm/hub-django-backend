"""CF Access JWT verification + JWKS cache.

Verifies the ``CF-Access-Jwt-Assertion`` header signed by Cloudflare Access.
The JWKS endpoint is fetched on first use and cached for up to 1 hour
(configurable via ``CF_ACCESS_JWKS_CACHE_SECONDS``). The cache is process-
local and resets on worker restart — acceptable since CF rotates keys
infrequently.
"""

import json
import time
from typing import Any
from urllib.request import urlopen

import jwt

# In-process JWKS cache. Keyed by URL so multiple teams / audiences stay
# isolated. Each value is (fetched_at_monotonic, jwks_dict).
_jwks_cache: dict[str, tuple[float, dict[str, Any]]] = {}

DEFAULT_CACHE_SECONDS = 3600


def get_jwks(url: str, cache_seconds: int = DEFAULT_CACHE_SECONDS) -> dict[str, Any]:
    """Fetch + cache the JWKS document."""
    now = time.monotonic()
    cached = _jwks_cache.get(url)
    if cached is not None and (now - cached[0]) < cache_seconds:
        return cached[1]
    with urlopen(url, timeout=5) as resp:  # noqa: S310 — trusted CF Access URL from settings
        raw = resp.read()
    data: dict[str, Any] = json.loads(raw)
    _jwks_cache[url] = (now, data)
    return data


def clear_jwks_cache() -> None:
    """Test helper. Also useful if keys rotate mid-run."""
    _jwks_cache.clear()


def verify_cf_access_jwt(token: str, *, jwks_url: str, audience: str) -> dict[str, Any]:
    """Verify a CF Access JWT and return the decoded claims.

    Raises ``jwt.InvalidTokenError`` (or a subclass) on any failure:
    missing kid, no matching key, bad signature, expired, wrong audience.
    """
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    if not kid:
        raise jwt.InvalidTokenError("jwt missing kid")

    jwks = get_jwks(jwks_url)
    key = None
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(k))
            break
    if key is None:
        raise jwt.InvalidTokenError(f"jwt kid {kid} not in JWKS")

    decoded: dict[str, Any] = jwt.decode(
        token,
        key=key,  # type: ignore[arg-type]  # JWK always yields a public key here
        algorithms=["RS256"],
        audience=audience,
    )
    return decoded
