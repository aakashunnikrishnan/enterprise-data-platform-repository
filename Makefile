.PHONY: install test lint format check

install:
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest

test-coverage:
	pytest --cov --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

check:
	ruff check .
	ruff format --check .
	pytest

compose-up:
	docker compose up -d

compose-down:
	docker compose down

compose-build:
	docker compose build

compose-rebuild:
	docker compose build --no-cache

compose-logs:
	docker compose logs -f

compose-ps:
	docker compose ps

kafka-topics:
	docker compose exec kafka \
		/opt/kafka/bin/kafka-topics.sh \
		--bootstrap-server kafka:29092 \
		--list

test:
	pytest -v

check:
	pre-commit run --all-files
	pytest -v
