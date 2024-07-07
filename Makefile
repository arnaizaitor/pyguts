#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available targets:"
	@echo "black		$$(tput sgr0)Run Black formatter"
	@echo "lint		$$(tput sgr0)Run pylint and Flake8"
	@echo "coverage	$$(tput sgr0)Run coverage"
	@echo "test		$$(tput sgr0)Run tests"
	@echo "clean		$$(tput sgr0)Clean generated files"
	@echo "all 		$$(tput sgr0)Run all targets"

#################################################################################
# Recipes                                                                       #
#################################################################################

# Define the paths to your Python files
PYTHON_FILES := **/*.py

# Define the target to run Black formatter
black:
	@echo "Running Black formatter..."
	@python3 -m black .

# Define the targets to run pylint and Flake8
lint:
	@echo "Running pylint..."
	@pylint $(PYTHON_FILES)
	@echo "Running Flake8..."
	@flake8 $(PYTHON_FILES)

coverage:
	@echo "Running coverage..."
	@coverage run -m unittest discover -s . -p '*.py' -v
	@coverage report -m
	@coverage html

test:
	@echo "Running tests..."
	@pytest

# Define the target to clean generated files
clean:
	@echo "Cleaning pytest cache..."
	@if [ -d .pytest_cache ]; then rm -r .pytest_cache; fi
	@echo "Cleaning log files..."
	@python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.log')]"
	@echo "Cleaning Python cache files..."
	@python3 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	@echo "Cleaning Python cache directories..."
	@python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

run:
	@echo "Running the application..."
	@python3 pyguts/__main__.py ./examples

all: black lint coverage test clean