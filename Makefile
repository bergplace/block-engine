help:
	less help-msg

dev: use-custom-conf build-block-engine-dev down-dev run-block-engine-dev

prod: use-custom-conf build-block-engine-prod down-prod run-block-engine-prod

# DEV

down-dev:
	docker-compose down -v

build-block-engine-dev:
	docker-compose build mongo mongo-express block-engine

run-block-engine-dev:
	docker-compose up mongo mongo-express block-engine

# PROD

down-prod:
	docker-compose down -v

build-block-engine-prod:
	docker-compose build mongo block-engine

run-block-engine-prod:
	docker-compose up -d mongo block-engine

# UTILS

block-engine-shell:
	docker-compose exec block-engine bash

use-custom-conf:
	cp block-engine.conf .env
