# Sprint Mode Hub — local dev targets.
#
# All commands run from the repo root.

COMPOSE := docker compose -f local-dev/docker-compose.yml

.PHONY: local-up local-down local-logs local-shell local-migrate local-seed reload-routing verify-TKT-010 verify-TKT-011 verify-TKT-012 verify-TKT-013 verify-TKT-014 verify-TKT-015 verify-TKT-017 verify-TKT-018 verify-TKT-019 verify-TKT-020 verify-TKT-021 verify-ticket

local-up:
	python local-dev/caddy/build_caddyfile.py
	$(COMPOSE) up -d --build

local-down:
	$(COMPOSE) down -v

local-logs:
	$(COMPOSE) logs -f

local-shell:
	$(COMPOSE) exec django bash

local-migrate:
	$(COMPOSE) exec django python manage.py migrate

local-seed:
	$(COMPOSE) exec django python manage.py loaddata fixtures/seed_hub_sprint_mode.json

reload-routing:
	python local-dev/caddy/build_caddyfile.py
	$(COMPOSE) exec caddy caddy reload --config /etc/caddy/Caddyfile

# Validate the compose file without pulling images.
verify-TKT-010:
	@$(COMPOSE) config >/dev/null && echo "docker-compose.yml OK (syntax valid, images not pulled)"
	@test -f local-dev/Dockerfile.django && echo "Dockerfile.django present"
	@test -f local-dev/.env.example && echo ".env.example present"
	@test -f local-dev/README.md && echo "README.md present"

verify-TKT-011:
	python local-dev/caddy/build_caddyfile.py --check
	pytest local-dev/caddy/tests/test_build_caddyfile.py
	@$(COMPOSE) config >/dev/null && echo "docker-compose.yml OK (caddy service valid)"

verify-TKT-012:
	node --check local-dev/mock-legacy/server.js
	node --test local-dev/mock-legacy/tests/*.test.js
	@$(COMPOSE) config >/dev/null && echo "docker-compose.yml OK (mock-legacy service valid)"

verify-TKT-013:
	pytest tools/tests/test_capture_fixtures.py
	python tools/capture_fixtures.py --help >/dev/null

verify-TKT-014:
	pytest tests/fixtures/test_manifest_coverage.py

verify-TKT-015:
	pytest tests/contract/test_template.py

verify-TKT-017:
	npm --prefix local-dev/playwright ci
	npm --prefix local-dev/playwright exec playwright -- test --config local-dev/playwright/playwright.config.ts local-dev/playwright/tickets/TKT-EXAMPLE.spec.ts

verify-TKT-018:
	pytest tests/test_seed_sanitized.py
	python tools/capture_seed.py --output /tmp/hub-seed-smoke.json

verify-TKT-019:
	@set -eu; \
		container=hub_tkt019_postgres; \
		cleanup() { docker rm -f "$$container" >/dev/null 2>&1 || true; }; \
		cleanup; \
		docker run --name "$$container" \
			-e POSTGRES_USER=hub \
			-e POSTGRES_PASSWORD=hub \
			-e POSTGRES_DB=hub_tkt019 \
			-d pgvector/pgvector:pg16 >/dev/null; \
		trap cleanup EXIT; \
		for _ in $$(seq 1 60); do \
			if docker logs "$$container" 2>&1 | grep -q "PostgreSQL init process complete"; then \
				break; \
			fi; \
			sleep 1; \
		done; \
		for _ in $$(seq 1 30); do \
			if docker exec "$$container" pg_isready -U hub -d hub_tkt019 >/dev/null 2>&1; then \
				break; \
			fi; \
			sleep 1; \
		done; \
		docker exec "$$container" pg_isready -U hub -d hub_tkt019 >/dev/null; \
		docker exec -i "$$container" psql -U hub -d hub_tkt019 -v ON_ERROR_STOP=1 < migrations/initial/schema.sql; \
		count="$$(docker exec "$$container" psql -U hub -d hub_tkt019 -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d '[:space:]')"; \
		test "$$count" = "251" || (echo "expected 251 public tables from current source snapshot, got $$count" && exit 1); \
		echo "Postgres initial schema OK ($$count public tables)"

verify-TKT-020:
	@set -eu; \
		container=hub_tkt020_postgres; \
		inspectdb_out=/tmp/hub-tkt020-inspectdb.py; \
		cleanup() { docker rm -f "$$container" >/dev/null 2>&1 || true; }; \
		cleanup; \
		docker run --name "$$container" \
			-e POSTGRES_USER=hub \
			-e POSTGRES_PASSWORD=hub \
			-e POSTGRES_DB=hub_tkt020 \
			-p 127.0.0.1::5432 \
			-d pgvector/pgvector:pg16 >/dev/null; \
		trap cleanup EXIT; \
		for _ in $$(seq 1 60); do \
			if docker logs "$$container" 2>&1 | grep -q "PostgreSQL init process complete"; then \
				break; \
			fi; \
			sleep 1; \
		done; \
		for _ in $$(seq 1 30); do \
			if docker exec "$$container" pg_isready -U hub -d hub_tkt020 >/dev/null 2>&1; then \
				break; \
			fi; \
			sleep 1; \
		done; \
		docker exec "$$container" pg_isready -U hub -d hub_tkt020 >/dev/null; \
		docker exec -i "$$container" psql -U hub -d hub_tkt020 -v ON_ERROR_STOP=1 < migrations/initial/schema.sql >/tmp/hub-tkt020-schema-load.log; \
		port="$$(docker inspect -f '{{(index (index .NetworkSettings.Ports "5432/tcp") 0).HostPort}}' "$$container")"; \
		DATABASE_URL="postgres://hub:hub@127.0.0.1:$$port/hub_tkt020" python manage.py inspectdb > "$$inspectdb_out"; \
		python tools/verify_tkt020_models.py --inspectdb "$$inspectdb_out"
	python manage.py check
	mypy --strict apps/*/models.py

verify-TKT-021:
	python manage.py makemigrations --check --dry-run
	@set -eu; \
		container=hub_tkt021_postgres; \
		cleanup() { docker rm -f "$$container" >/dev/null 2>&1 || true; }; \
		cleanup; \
		docker run --name "$$container" \
			-e POSTGRES_USER=hub \
			-e POSTGRES_PASSWORD=hub \
			-e POSTGRES_DB=hub_tkt021 \
			-p 127.0.0.1::5432 \
			-d pgvector/pgvector:pg16 >/dev/null; \
		trap cleanup EXIT; \
		for _ in $$(seq 1 60); do \
			if docker logs "$$container" 2>&1 | grep -q "PostgreSQL init process complete"; then \
				break; \
			fi; \
			sleep 1; \
		done; \
		for _ in $$(seq 1 30); do \
			if docker exec "$$container" pg_isready -U hub -d hub_tkt021 >/dev/null 2>&1; then \
				break; \
			fi; \
			sleep 1; \
		done; \
		docker exec "$$container" pg_isready -U hub -d hub_tkt021 >/dev/null; \
		docker exec -i "$$container" psql -U hub -d hub_tkt021 -v ON_ERROR_STOP=1 < migrations/initial/schema.sql >/tmp/hub-tkt021-schema-load.log; \
		port="$$(docker inspect -f '{{(index (index .NetworkSettings.Ports "5432/tcp") 0).HostPort}}' "$$container")"; \
		DATABASE_URL="postgres://hub:hub@127.0.0.1:$$port/hub_tkt021" python manage.py migrate --fake-initial --noinput; \
		DATABASE_URL="postgres://hub:hub@127.0.0.1:$$port/hub_tkt021" python manage.py migrate --check

verify-ticket:
	@test -n "$(TKT)" || (echo "usage: make verify-ticket TKT=TKT-XXX" && exit 2)
	npm --prefix local-dev/playwright ci
	$(MAKE) local-up
	$(MAKE) local-migrate
	$(MAKE) local-seed
	npm --prefix local-dev/playwright exec playwright -- test --config local-dev/playwright/playwright.config.ts local-dev/playwright/tickets/$(TKT).spec.ts
