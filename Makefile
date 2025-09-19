# Antioch Organic Market - Django Project Makefile
# ================================================

.PHONY: help install setup migrate run dev clean test collectstatic superuser requirements

# Default Python and Django commands
PYTHON = python3
PIP = pip3
DJANGO = $(PYTHON) manage.py

# Virtual environment
VENV = venv
VENV_BIN = $(VENV)/bin
VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP = $(VENV_BIN)/pip

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Antioch Organic Market - Django Project$(NC)"
	@echo "========================================"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install Python dependencies
	@echo "$(YELLOW)Installing Python dependencies...$(NC)"
	$(PIP) install -r requirements.txt

venv: ## Create virtual environment
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Virtual environment created! Activate it with: source $(VENV)/bin/activate$(NC)"

install-venv: venv ## Install dependencies in virtual environment
	@echo "$(YELLOW)Installing dependencies in virtual environment...$(NC)"
	$(VENV_PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed in virtual environment!$(NC)"

setup: install migrate collectstatic ## Complete project setup
	@echo "$(GREEN)Project setup complete!$(NC)"
	@echo "$(YELLOW)Run 'make superuser' to create an admin user$(NC)"
	@echo "$(YELLOW)Run 'make run' to start the development server$(NC)"

migrate: ## Apply database migrations
	@echo "$(YELLOW)Applying database migrations...$(NC)"
	$(DJANGO) makemigrations
	$(DJANGO) migrate

collectstatic: ## Collect static files
	@echo "$(YELLOW)Collecting static files...$(NC)"
	$(DJANGO) collectstatic --noinput

superuser: ## Create Django superuser
	@echo "$(YELLOW)Creating Django superuser...$(NC)"
	$(DJANGO) createsuperuser

run: ## Run development server
	@echo "$(YELLOW)Starting Django development server...$(NC)"
	@echo "$(GREEN)Server will be available at: http://127.0.0.1:8000$(NC)"
	$(DJANGO) runserver

run-production: ## Run with Gunicorn (production)
	@echo "$(YELLOW)Starting Gunicorn server...$(NC)"
	gunicorn antioch.wsgi:application --bind 0.0.0.0:8000

dev: migrate run ## Quick development setup (migrate + run)

test: ## Run Django tests
	@echo "$(YELLOW)Running Django tests...$(NC)"
	$(DJANGO) test

shell: ## Open Django shell
	@echo "$(YELLOW)Opening Django shell...$(NC)"
	$(DJANGO) shell

makemigrations: ## Create new migrations
	@echo "$(YELLOW)Creating new migrations...$(NC)"
	$(DJANGO) makemigrations

flush: ## Clear database data
	@echo "$(RED)Warning: This will delete all data!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] && $(DJANGO) flush

reset-db: ## Reset database completely
	@echo "$(RED)Warning: This will delete the database file!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] && rm -f db.sqlite3 && make migrate

clean: ## Clean Python cache files
	@echo "$(YELLOW)Cleaning Python cache files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

install-redis: ## Install Redis (macOS)
	@echo "$(YELLOW)Installing Redis...$(NC)"
	@if command -v brew >/dev/null 2>&1; then \
		brew install redis; \
		echo "$(GREEN)Redis installed! Start with: brew services start redis$(NC)"; \
	else \
		echo "$(RED)Homebrew not found. Please install Redis manually.$(NC)"; \
	fi

start-redis: ## Start Redis server
	@echo "$(YELLOW)Starting Redis server...$(NC)"
	@if command -v brew >/dev/null 2>&1; then \
		brew services start redis; \
	else \
		redis-server; \
	fi

stop-redis: ## Stop Redis server
	@echo "$(YELLOW)Stopping Redis server...$(NC)"
	@if command -v brew >/dev/null 2>&1; then \
		brew services stop redis; \
	else \
		pkill redis-server || echo "Redis not running"; \
	fi

worker: ## Start Django-RQ worker
	@echo "$(YELLOW)Starting Django-RQ worker...$(NC)"
	$(DJANGO) rqworker default

requirements: ## Generate/update requirements.txt
	@echo "$(YELLOW)Generating requirements.txt...$(NC)"
	$(PIP) freeze > requirements.txt
	@echo "$(GREEN)requirements.txt updated!$(NC)"

check: ## Run Django system checks
	@echo "$(YELLOW)Running Django system checks...$(NC)"
	$(DJANGO) check

lint: ## Run basic Python linting (if available)
	@echo "$(YELLOW)Running Python linting...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 . --exclude=venv,migrations --max-line-length=88; \
	else \
		echo "$(YELLOW)flake8 not installed. Install with: pip install flake8$(NC)"; \
	fi

backup-db: ## Backup database
	@echo "$(YELLOW)Creating database backup...$(NC)"
	cp db.sqlite3 db.sqlite3.backup.$(shell date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)Database backed up!$(NC)"

status: ## Show project status
	@echo "$(GREEN)Antioch Organic Market - Project Status$(NC)"
	@echo "======================================"
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Django version: $(shell $(DJANGO) --version 2>/dev/null || echo 'Not installed')"
	@echo "Database: $(shell [ -f db.sqlite3 ] && echo 'SQLite (exists)' || echo 'SQLite (not created)')"
	@echo "Redis status: $(shell redis-cli ping 2>/dev/null || echo 'Not running')"
	@echo ""
	@echo "$(YELLOW)Quick start:$(NC)"
	@echo "1. make setup     # Setup project"
	@echo "2. make superuser # Create admin user"
	@echo "3. make run       # Start server"

# Development shortcuts
.PHONY: s m mm c r
s: run ## Shortcut for run
m: migrate ## Shortcut for migrate  
mm: makemigrations ## Shortcut for makemigrations
c: collectstatic ## Shortcut for collectstatic
r: requirements ## Shortcut for requirements