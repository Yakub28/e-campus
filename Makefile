.DEFAULT_GOAL := help

.PHONY = help install runserver migrate makemigrations createsuperuser test format lint cp-env

SETTINGS_FILENAME = pyproject.toml

help:
	@echo Please use 'make target' where target is one of
	@echo 	install           to install dependencies
	@echo 	runserver         to run the server
	@echo 	migrate           to run migrations
	@echo 	makemigrations    to make migrations
	@echo 	cp-env            to copy .env file

install:
	@echo "Installing dependencies..."
	poetry install

runserver:
	@echo "Starting server..."
	poetry run python manage.py runserver

migrate:
	@echo "Running migrations..."
	poetry run python manage.py migrate

makemigrations:
	@echo "Making migrations..."
	poetry run python manage.py makemigrations

createsuperuser:
	@echo "Creating superuser..."
	poetry run python manage.py createsuperuser

test:
	@echo "Running tests..."
	poetry run python manage.py test

format:
	@echo "Formatting code..."
	poetry run black . --config ${SETTINGS_FILENAME}
	poetry run isort . --settings-file ${SETTINGS_FILENAME}
	poetry run autoflake .

lint:
	@echo "Linting code..."
	poetry run black . --check --diff --config ${SETTINGS_FILENAME}
	poetry run isort . --check --diff --settings-file ${SETTINGS_FILENAME}
	poetry run flake8 . --max-complexity 5 --toml-config ${SETTINGS_FILENAME}

cp-env:
	@echo "Copying .env file..."
ifdef OS
	copy .\config\.env.example .\config\.env
else
	cp ./config/.env.example ./config/.env
endif
