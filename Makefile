PYTHON := python3
PIP := $(PYTHON) -m pip

.PHONY: install run debug clean lint lint-strict

install:
        $(PIP) install -U mypy # flake8 pydantic numpy tortch


run:
        $(PYTHON) main.py

debug:
        $(PYTHON) -m pdb main.py

clean:
        rm -rf __pycache__ .mypy_cache .pytest_cache

lint:
        flake8 .
        mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
        flake8 .
        mypy . --strict