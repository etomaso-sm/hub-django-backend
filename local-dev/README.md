# Local dev infrastructure

docker-compose stack for running the Sprint Mode Hub backend locally. Lives
alongside the Django project; everything runs under `/local-dev/`.

## Prerequisites
- Docker Desktop (or any Docker Engine + compose v2).
- A copy of `.env` at `local-dev/.env` (copy from `.env.example`).

## Quick start

From the repo root:

```
make local-up         # build + start the stack in the background
make local-logs       # tail logs
make local-down       # stop and remove volumes
```

What comes up (as of TKT-010):
- **Postgres 16** (pgvector image) on `localhost:5432` - user `hub`, password `hub`, db `hub`.
- **Redis 7** on `localhost:6379`.
- **Django (ASGI)** on `localhost:8000` with `--reload` so edits in the host repo refresh the running process.

What will come up in later tickets:
- TKT-011: Caddy reverse proxy on `:8080` (the local strangler).
- TKT-012: Mock-legacy worker on `:8787` (fixture replay).
- TKT-017: Vite frontend dev server on `:5173` (against solid-sheep sources).

## First run

```
make local-up
docker compose -f local-dev/docker-compose.yml exec django python manage.py migrate
docker compose -f local-dev/docker-compose.yml exec django python manage.py loaddata fixtures/dev_seed.json
```

Then hit `http://localhost:8000/admin/` — Django should respond (anonymous
view until you create a superuser the Django way, but the TCP stack is
healthy).

## Verify the compose file without pulling images

```
make verify-TKT-010
```

Runs `docker compose config` in validate-only mode. Does not pull
multi-gigabyte images or start anything. Useful for CI.

## pgvector

The `pgvector/pgvector:pg16` image ships with the extension pre-built.
After `migrate`, the extension is available; the app will `CREATE EXTENSION
IF NOT EXISTS vector;` when TKT-047 (vectorize app) lands.
