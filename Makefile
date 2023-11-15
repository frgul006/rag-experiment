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

.PHONY: scrape
scrape:
	PYTHONPATH=. pipenv run python regent_rag/scrape.py

.PHONY: splits
splits:
	PYTHONPATH=. pipenv run python regent_rag/splits.py

.PHONY: embeddings
embeddings:
	PYTHONPATH=. pipenv run python regent_rag/embeddings.py

.PHONY: retrieval
retrieval:
	PYTHONPATH=. pipenv run python regent_rag/retrieval.py

.PHONY: evaluation
evaluation:
	PYTHONPATH=. pipenv run python regent_rag/evaluation.py

.PHONY: flask
flask:
	PYTHONPATH=. pipenv run flask run