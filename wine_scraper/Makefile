.PHONY: help install run-service run-dry-run run-batch-test run-single clean lint test

# Default target
help:
	@echo "Wine Scraper Service - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install        - Create venv and install dependencies"
	@echo "  run-service    - Start RabbitMQ service mode"
	@echo "  run-dry-run    - Start service in dry-run mode (interactive)"
	@echo "  run-batch-test - Test scraping with sample wineries"
	@echo "  run-single     - Test scraping a single winery"
	@echo "  clean          - Clean cache and temporary files"
	@echo "  lint           - Run code linting"
	@echo "  test           - Run basic tests"
	@echo ""
	@echo "Usage examples:"
	@echo "  make install"
	@echo "  make run-dry-run"
	@echo "  make run-batch-test"

# Python and virtual environment
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Check if virtual environment exists
VENV_EXISTS = $(wildcard $(VENV)/bin/activate)

# Create virtual environment and install dependencies
install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "✅ Installation complete!"
	@echo "To activate the virtual environment: source $(VENV)/bin/activate"

$(VENV)/bin/activate:
	@echo "📦 Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "📥 Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Start RabbitMQ service mode
run-service: check-venv
	@echo "🚀 Starting RabbitMQ service mode..."
	$(PYTHON) -m orchestration.__main__ start

# Start service in dry-run mode (interactive)
run-dry-run: check-venv
	@echo "🧪 Starting service in dry-run mode..."
	$(PYTHON) -m orchestration.__main__ start --dry-run

# Test scraping with sample wineries
run-batch-test: check-venv
	@echo "🧪 Testing batch scraping with sample wineries..."
	$(PYTHON) cli.py batch-scrape test_wineries.txt --dry-run

# Test scraping a single winery
run-single: check-venv
	@echo "🧪 Testing single winery scraping..."
	$(PYTHON) demo_single.py

# Clean cache and temporary files
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	-$(PYTHON) cli.py clean-cache 2>/dev/null || true
	-find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	-find . -type f -name "*.pyc" -delete 2>/dev/null || true
	-rm -rf .cache 2>/dev/null || true
	rm -rf data 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Run code linting
lint: check-venv
	@echo "🔍 Running code linting..."
	-$(PYTHON) -m flake8 . --exclude=$(VENV) --max-line-length=100 2>/dev/null || echo "flake8 not available"
	-$(PYTHON) -m pylint *.py scrapers/ orchestration/ pipelines/ utils/ --ignore=$(VENV) 2>/dev/null || echo "pylint not available"

# Run basic tests
test: check-venv
	@echo "🧪 Running basic tests..."
	$(PYTHON) test_simple.py

# Ensure virtual environment exists
check-venv:
	@if [ -z "$(VENV_EXISTS)" ]; then \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi

# Development utilities
dev-setup: install
	@echo "🔧 Installing development dependencies..."
	$(PIP) install flake8 pylint pytest black isort

# Format code
format: check-venv
	@echo "🎨 Formatting code..."
	-$(PYTHON) -m black . --exclude=$(VENV) 2>/dev/null || echo "black not available"
	-$(PYTHON) -m isort . --skip $(VENV) 2>/dev/null || echo "isort not available"