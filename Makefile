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
