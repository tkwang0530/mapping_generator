# Makefile for Dictionary Checker and Mapping Generator

# Variables
PYTHON=python
CHECK_SCRIPT=check.py
MAIN_SCRIPT=main.py

# Default target
.PHONY: all
all: map

# Target to run checks
.PHONY: check
check:
	$(PYTHON) $(CHECK_SCRIPT)

# Target to run mapping generator
.PHONY: map
map:
	$(PYTHON) $(MAIN_SCRIPT)

# Clean target (if needed)
.PHONY: clean
clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -f .map*

# Help target
.PHONY: help
help:
	@echo "Makefile for Dictionary Checker and Mapping Generator"
	@echo "Usage:"
	@echo "  make check            Run the checks"
	@echo "  make map              Run the mapping generator"
	@echo "  make clean            Clean up generated files"
	@echo "  make help             Show this help message"