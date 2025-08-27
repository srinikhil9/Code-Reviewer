# AI Code Review Assistant - Development Makefile
.PHONY: help install install-dev test lint format clean run-example run-langgraph docs build check-all

# Default target
help: ## Show this help message
	@echo "AI Code Review Assistant - Development Commands"
	@echo "================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation commands
install: ## Install project dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e .[dev,test]

# Code quality commands
format: ## Format code with black and sort imports
	black .
	ruff check . --fix --select I

lint: ## Run linting checks
	ruff check .
	black --check .

lint-fix: ## Run linting and fix issues
	ruff check . --fix
	black .

# Testing commands
test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=flows --cov-report=html --cov-report=term

test-fast: ## Run tests excluding slow tests
	pytest tests/ -v -m "not slow"

# Development server commands
run-langflow: ## Start Langflow server
	langflow run --host 0.0.0.0 --port 7860

run-example: ## Run example usage script
	python example_usage.py

run-langgraph: ## Run LangGraph flow with default task
	python -m flows.run_langgraph "Create a Python function that validates email addresses using regex"

run-langgraph-interactive: ## Run LangGraph flow with human input enabled
	ALLOW_HUMAN_INPUT=1 python -m flows.run_langgraph "Implement an LRU cache in Python"

# Documentation commands
docs-serve: ## Serve documentation locally (if using mkdocs)
	@echo "Documentation serving not yet configured. See README.md for manual docs."

# Build commands
build: ## Build the project (if packaging)
	python -m build

# Utility commands
clean: ## Clean up temporary files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f batch_results.json

# Comprehensive check
check-all: lint test ## Run all checks (linting and tests)

# Environment setup
setup-env: ## Set up development environment
	@echo "Setting up development environment..."
	@echo "1. Creating virtual environment..."
	python -m venv venv
	@echo "2. Please activate the virtual environment:"
	@echo "   - Windows: venv\\Scripts\\activate"
	@echo "   - macOS/Linux: source venv/bin/activate"
	@echo "3. Then run: make install-dev"
	@echo "4. Copy .env.example to .env and add your API keys"

# Git hooks
install-hooks: ## Install git pre-commit hooks
	@echo "Installing git hooks..."
	@echo "#!/bin/sh" > .git/hooks/pre-commit
	@echo "make check-all" >> .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "Pre-commit hooks installed!"

# Development workflow
dev-setup: install-dev install-hooks ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "Run 'make run-langgraph' to test the setup."

# Security checks
security-check: ## Run security checks
	@command -v safety >/dev/null 2>&1 || { echo "Installing safety..."; pip install safety; }
	@command -v bandit >/dev/null 2>&1 || { echo "Installing bandit..."; pip install bandit; }
	safety check
	bandit -r flows/ -f json

# Project info
info: ## Show project information
	@echo "AI Code Review Assistant"
	@echo "======================="
	@echo "Python version: $$(python --version)"
	@echo "Project structure:"
	@find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" | head -10
	@echo "Dependencies:"
	@pip list | grep -E "(langchain|langgraph|openai)" || echo "Dependencies not installed"
