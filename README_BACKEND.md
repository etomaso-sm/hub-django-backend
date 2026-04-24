# Sprint Mode Hub - Django Backend

Local-dev Django + DRF backend that will replace the current Cloudflare Workers
backend serving the heyhub.ai frontend. The migration is executed ticket-by-ticket
following `MIGRATION_TICKETS.md` (lives in the sibling `solid-sheep` worktree).

## North star

The React frontend at heyhub.ai must keep working exactly as it does today.
No user-visible change. Every ticket is gated by a Playwright scenario that
drives the real UI against the new backend (localhost) and asserts behavior
equivalence with production.

## Quick start

```bash
# from the repo root
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python manage.py check
```

Full local dev loop (docker, postgres, redis, caddy, frontend) arrives in TKT-010.
See `local-dev/README.md` once that ticket lands.

## Branching

- **Working branch:** `development`. All PRs target this.
- **`main`:** reserved for stable milestones, set manually by Eugenio.
- **Feature branches:** `migration/TKT-XXX-slug`.

## Origin

`git@github.com:etomaso-sm/hub-django-backend.git`

The autopilot must never push to any other origin, and must never push from the
`solid-sheep` worktree. See the "Execution rules" section of `MIGRATION_TICKETS.md`.

## Status

Initial scaffold from TKT-001. No apps, no routes, no models yet - those land
per-ticket starting TKT-002.
