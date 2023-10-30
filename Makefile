SOURCE_FOLDER = regent_rag

.PHONY: install-dev
install-dev:
	PYTHONPATH=. pipenv sync --dev

.PHONY: format
format:
	PYTHONPATH=. pipenv run isort $(SOURCE_FOLDER) tests/*
	PYTHONPATH=. pipenv run black $(SOURCE_FOLDER) tests

.PHONY: test
test:
	PYTHONPATH=. pipenv run python -m pytest tests

.PHONY: lint
lint:
	PYTHONPATH=. pipenv run pycodestyle .
	PYTHONPATH=. pipenv run isort --check-only $(SOURCE_FOLDER) tests/*
	PYTHONPATH=. pipenv run black --check $(SOURCE_FOLDER) tests
	PYTHONPATH=. pipenv run pylint $(SOURCE_FOLDER)
	PYTHONPATH=. pipenv run pylint tests/*
	PYTHONPATH=. pipenv run mypy $(SOURCE_FOLDER)

.PHONY: scrape
scrape:
	PYTHONPATH=. pipenv run python regent_rag/scraper.py

.PHONY: chunks
chunks:
	PYTHONPATH=. pipenv run python regent_rag/chunker.py

.PHONY: vectors
vectors:
	PYTHONPATH=. pipenv run python regent_rag/vectorizor.py

.PHONY: query
query:
	PYTHONPATH=. pipenv run python regent_rag/query.py