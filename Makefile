install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

lint:
	poetry run flake8 page_loader

build:
	poetry build