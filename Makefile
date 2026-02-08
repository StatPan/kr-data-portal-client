.PHONY: install test lint format ci help

help:
	@echo "Usage: make <target>"
	@echo "  install  Install dependencies and pre-commit hooks"
	@echo "  test     Run tests"
	@echo "  lint     Run linter (ruff)"
	@echo "  format   Run formatter (ruff)"
	@echo "  ci       Run all checks (lint + test)"

install:
	uv sync --all-extras
	uv run pre-commit install

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

ci: lint test
