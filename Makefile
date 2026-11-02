.PHONY: develop requirements build install lint lint-py lint-docs fix fix-py fix-docs format checks check check-dist check-types test tests coverage dist dist-build dist-check show-version patch minor major clean help

develop:  ## install the library and development dependencies
	uv pip install -e '.[develop]'

requirements:  ## install development requirements
	uv pip install -r pyproject.toml --extra develop

build:  ## build Python distributions
	python -m build -n

install:  ## install the library
	uv pip install .

lint-py:  ## lint Python
	python -m ruff check ipydagred3
	python -m ruff format --check ipydagred3

lint-docs:  ## lint documentation
	python -m mdformat --check README.md CONTRIBUTING.md docs/compatibility.md
	python -m codespell_lib README.md CONTRIBUTING.md docs/compatibility.md

lint: lint-py lint-docs  ## run linters
lints: lint

fix-py:  ## format Python
	python -m ruff check --fix ipydagred3
	python -m ruff format ipydagred3

fix-docs:  ## format documentation
	python -m mdformat README.md CONTRIBUTING.md docs/compatibility.md

fix: fix-py fix-docs  ## run formatters
format: fix

check-dist:  ## validate Python distribution contents
	check-dist -v

check-types:  ## check Python types
	python -m ty check

checks: check-dist check-types  ## run package and type checks
check: checks

test:  ## run Python tests
	python -m pytest ipydagred3/tests

tests: test

coverage:  ## run tests with coverage
	python -m pytest ipydagred3/tests --cov=ipydagred3 --cov-report=term-missing --cov-report=xml

dist-build:  ## build wheel and source distribution
	python -m build -w -s

dist-check:  ## check distribution metadata
	python -m twine check dist/*

dist: dist-build dist-check  ## build and validate distributions

show-version:  ## show current version
	bump-my-version show current_version

patch minor major:  ## bump version
	bump-my-version bump $@

clean:  ## remove generated build and test artifacts
	rm -rf build dist .coverage coverage.xml junit.xml .pytest_cache .ruff_cache

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
