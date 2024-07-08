.POSIX:

NAME = ml_engineer_task
PYTHON_VERSION = 3.12.2

POETRY = python -m poetry
PYTEST = python -m pytest

help:
	@printf "activate \n\
	TODO \n"

activate:
	@echo "pyenv activate $(NAME)"

poetry-bootstrap:
# black, isort, flake8 for dev
	@printf "Only used once at the start of the project.\nPlease note: If you already have a pyproject.toml file, you do not want to do this step\n"
	@echo "$(POETRY) init"

lint:
	python -m black -l 200 .
	python -m isort --profile black .
	python -m flake8 --ignore E501,F401,F403,F405 .

pyenv:
	@echo "pyenv virtualenv $(PYTHON_VERSION) $(NAME)"
	@echo "\`make activate\`"
	@echo "pip install poetry"
	@echo "$(POETRY) install"

test:
	$(PYTEST) -vs -vv

dev:
	$(PYTEST) -vs -vv -k 'test_dev'

psql:
	@echo psql -U postgres -h ${HOST} -d $(DBNAME)

schema:
	@echo TODO
	@echo pg_dump -U postgres -s -h ${HOST} -t $(TABLE) -d $(DBNAME)

pre-commit: lint test requirements
