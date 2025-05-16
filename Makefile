.PHONY: setup install test lint format clean run-api

setup:
	poetry install

install:
	poetry install --no-dev

test:
	poetry run pytest tests/ -v

lint:
	poetry run flake8 src/ tests/
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/
	poetry run mypy src/ tests/

format:
	poetry run black src/ tests/
	poetry run isort src/ tests/

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

{% if cookiecutter.include_fastapi == "yes" %}
run-api:
	poetry run uvicorn src.interfaces.api.main:app --reload
{% endif %} 