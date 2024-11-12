PYTHON = python
DJANGO_PROJECT = rentnbook

VENV_DIR = venv
PIP = $(VENV_DIR)/Scripts/pip
DJANGO_MANAGE = $(VENV_DIR)/Scripts/python $(DJANGO_PROJECT)/manage.py

# Install dependencies
install:
	@echo "Installing dependencies..."
	@python3 -m venv $(VENV_DIR)
	@$(PIP) install -r requirements.txt

# Make migrations
makemigrations:
	@echo "Making migrations..."
	@$(DJANGO_MANAGE) makemigrations

# Run migrations
migrate:
	@echo "Running migrations..."
	@$(DJANGO_MANAGE) migrate

# Create a superuser
createsuperuser:
	@echo "Creating superuser..."
	@$(DJANGO_MANAGE) createsuperuser

# Run the development server
run:
	@echo "Starting development server..."
	@$(DJANGO_MANAGE) runserver

# Collect static files
collectstatic:
	@echo "Collecting static files..."
	@$(DJANGO_MANAGE) collectstatic --noinput

# Test the project
test:
	@echo "Running tests..."
	@$(DJANGO_MANAGE) test

.PHONY: install makemigrations migrate createsuperuser run collectstatic test
