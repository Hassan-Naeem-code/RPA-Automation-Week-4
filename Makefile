# Flight Automation System - Development Makefile

.PHONY: help install install-dev test test-cov lint format type-check security clean build docker run docs

# Variables
PYTHON := python3
PIP := pip3
PACKAGE_NAME := flight_automation
TEST_PATH := tests/
SOURCE_PATH := flight_automation/ scripts/

# Default target
help: ## Show this help message
	@echo "Flight Automation System - Development Commands"
	@echo "================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation
install: ## Install production dependencies
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

install-hooks: ## Install pre-commit hooks
	pre-commit install

# Testing
test: ## Run unit tests
	pytest $(TEST_PATH) -v

test-cov: ## Run tests with coverage report
	pytest $(TEST_PATH) --cov=$(PACKAGE_NAME) --cov-report=html --cov-report=term-missing

test-integration: ## Run integration tests
	pytest $(TEST_PATH) -m integration -v

test-all: ## Run all tests including slow ones
	pytest $(TEST_PATH) -v --runslow

# Code Quality
lint: ## Run linting (flake8)
	flake8 $(SOURCE_PATH) $(TEST_PATH)

format: ## Format code with black and isort
	black $(SOURCE_PATH) $(TEST_PATH)
	isort $(SOURCE_PATH) $(TEST_PATH)

format-check: ## Check if code formatting is correct
	black --check $(SOURCE_PATH) $(TEST_PATH)
	isort --check-only $(SOURCE_PATH) $(TEST_PATH)

type-check: ## Run type checking with mypy
	mypy $(SOURCE_PATH) --ignore-missing-imports

security: ## Run security checks with bandit
	bandit -r $(PACKAGE_NAME) -f json -o reports/bandit-report.json

# Pre-commit
pre-commit: ## Run all pre-commit hooks
	pre-commit run --all-files

# Build and Distribution
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## Build distribution packages
	$(PYTHON) -m build

build-wheel: clean ## Build wheel package only
	$(PYTHON) -m build --wheel

# Docker
docker-build: ## Build Docker image
	docker build -t flight-automation:latest .

docker-run: ## Run Docker container
	docker run --rm -it \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/logs:/app/logs \
		-v $(PWD)/reports:/app/reports \
		flight-automation:latest

docker-compose-up: ## Start services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose down

docker-compose-logs: ## View docker-compose logs
	docker-compose logs -f

# Application
run: ## Run the automation system
	$(PYTHON) scripts/run_automation.py

run-optimized: ## Run with optimization enabled
	$(PYTHON) scripts/run_automation.py --optimize

generate-data: ## Generate sample test data
	$(PYTHON) scripts/generate_data.py

profile: ## Run with profiling
	$(PYTHON) -m cProfile -o automation_profile.prof scripts/run_automation.py

# Documentation
docs: ## Generate documentation
	@echo "Generating documentation..."
	@mkdir -p docs/build
	@echo "Documentation generated in docs/build/"

docs-serve: ## Serve documentation locally
	@echo "Serving documentation on http://localhost:8000"
	@cd docs && $(PYTHON) -m http.server 8000

# Development
dev-setup: install-dev install-hooks ## Complete development setup
	@echo "Development environment setup complete!"

dev-test: format lint type-check test ## Run development test suite

dev-clean: clean ## Clean development environment
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf logs/*.log
	rm -rf reports/*.csv
	rm -rf reports/*.json

# Monitoring
monitor-logs: ## Monitor application logs
	tail -f logs/automation.log

monitor-performance: ## Monitor performance logs
	tail -f logs/performance.log

# Database (for future use)
db-init: ## Initialize database
	@echo "Database initialization not implemented yet"

db-migrate: ## Run database migrations
	@echo "Database migrations not implemented yet"

# Deployment
deploy-staging: ## Deploy to staging environment
	@echo "Staging deployment not implemented yet"

deploy-prod: ## Deploy to production environment
	@echo "Production deployment not implemented yet"

# Quality Gates
quality-gate: format-check lint type-check security test-cov ## Run all quality checks

ci-test: install-dev quality-gate ## CI test pipeline

# Information
info: ## Show project information
	@echo "Flight Automation System"
	@echo "========================"
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Package version: $(shell $(PYTHON) -c 'import flight_automation; print(flight_automation.__version__)' 2>/dev/null || echo 'Not installed')"
	@echo "Install location: $(shell $(PIP) show $(PACKAGE_NAME) | grep Location | cut -d' ' -f2 2>/dev/null || echo 'Not installed')"
