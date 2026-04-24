# Sprint Mode Hub — local dev targets.
#
# All commands run from the repo root.

COMPOSE := docker compose -f local-dev/docker-compose.yml

.PHONY: local-up local-down local-logs local-shell local-migrate local-seed reload-routing verify-TKT-010 verify-TKT-011 verify-TKT-012

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
	$(COMPOSE) exec django python manage.py loaddata fixtures/dev_seed.json

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
