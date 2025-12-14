SHELL := /bin/sh

.PHONY: up down logs test seed load

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

test:
	pytest -q || true

seed:
	python scripts/load.py --seed-only

load:
	python scripts/load.py --stress 250 --concurrent

