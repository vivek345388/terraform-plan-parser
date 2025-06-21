# Terraform Plan Parser Makefile

.PHONY: help install install-dev test lint format clean demo run-example

# Default target
help:
	@echo "Terraform Plan Parser - Available commands:"
	@echo ""
	@echo "  install      - Install the package in production mode"
	@echo "  install-dev  - Install the package in development mode"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean up build artifacts"
	@echo "  demo         - Run the demo script"
	@echo "  run-example  - Run example with sample plan"
	@echo ""

# Install the package
install:
	pip install -r requirements.txt
	pip install -e .

# Install in development mode
install-dev:
	pip install -r requirements.txt
	pip install -e .
	pip install pytest pytest-cov black flake8

# Run tests
test:
	python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Run linting
lint:
	flake8 src/ tests/ --max-line-length=88 --ignore=E203,W503
	python -m black --check src/ tests/

# Format code
format:
	black src/ tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Run demo script
demo:
	python examples/demo.py

# Run example with sample plan
run-example:
	python -m src.main examples/sample_plan.json

# Run example with detailed output
run-example-detailed:
	python -m src.main examples/sample_plan.json --detailed

# Run example with JSON output
run-example-json:
	python -m src.main examples/sample_plan.json --output-format json

# Run example with table output
run-example-table:
	python -m src.main examples/sample_plan.json --output-format table

# Run example with natural language output
run-example-natural:
	python -m src.main examples/sample_plan.json --output-format natural

# Run example with narrative output
run-example-narrative:
	python -m src.main examples/sample_plan.json --output-format narrative

# Run example with human-readable output
run-example-human:
	python -m src.main examples/sample_plan.json --output-format human

# Run example with natural language detailed output
run-example-natural-detailed:
	python -m src.main examples/sample_plan.json --output-format natural --detailed

# Run example with narrative detailed output
run-example-narrative-detailed:
	python -m src.main examples/sample_plan.json --output-format narrative --detailed

# Run example with human-readable detailed output
run-example-human-detailed:
	python -m src.main examples/sample_plan.json --output-format human --detailed

# Generate a new plan (requires terraform)
generate-plan:
	python -m src.main generate --auto-parse

# Show version
version:
	python -m src.main --version

# Build distribution
build:
	python setup.py sdist bdist_wheel

# Install from distribution
install-dist:
	pip install dist/*.whl 