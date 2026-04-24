# Sprint Mode Hub — local dev targets.
#
# All commands run from the repo root.

COMPOSE := docker compose -f local-dev/docker-compose.yml

.PHONY: local-up local-down local-logs local-shell local-migrate local-seed verify-TKT-010

local-up:
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

# Validate the compose file without pulling images.
verify-TKT-010:
	@$(COMPOSE) config >/dev/null && echo "docker-compose.yml OK (syntax valid, images not pulled)"
	@test -f local-dev/Dockerfile.django && echo "Dockerfile.django present"
	@test -f local-dev/.env.example && echo ".env.example present"
	@test -f local-dev/README.md && echo "README.md present"
