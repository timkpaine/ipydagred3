#########
# BUILD #
#########
.PHONY: develop build install

develop:  ## install dependencies and build library
	uv pip install -e .[develop]

requirements:  ## install prerequisite python build requirements
	uv pip install -r pyproject.toml --extra develop

build:  ## build the python library
	python -m build -n

install:  ## install library
	uv pip install .

#########
# LINTS #
#########
.PHONY: lint-py lint-docs fix-py fix-docs lint lints fix format

lint-py:  ## lint python with ruff
	python -m ruff check ipydagred3
	python -m ruff format --check ipydagred3

lint-docs:  ## lint docs with mdformat and codespell
	python -m mdformat --check README.md CONTRIBUTING.md docs/compatibility.md
	python -m codespell_lib README.md CONTRIBUTING.md docs/compatibility.md

fix-py:  ## autoformat python code with ruff
	python -m ruff check --fix ipydagred3
	python -m ruff format ipydagred3

fix-docs:  ## autoformat docs with mdformat and codespell
	python -m mdformat README.md CONTRIBUTING.md docs/compatibility.md
	python -m codespell_lib --write README.md CONTRIBUTING.md docs/compatibility.md

lint: lint-py lint-docs  ## run all linters
lints: lint
fix: fix-py fix-docs  ## run all autoformatters
format: fix

################
# Other Checks #
################
.PHONY: check-dist check-types checks check

check-dist:  ## check python sdist and wheel with check-dist
	check-dist -v

check-types:  ## check python types with ty
	python -m ty check

checks: check-dist check-types

# Alias
check: checks

#########
# TESTS #
#########
.PHONY: test coverage tests

test:  ## run python tests
	python -m pytest -v ipydagred3/tests

coverage:  ## run tests and collect test coverage
	python -m pytest -v ipydagred3/tests --cov=ipydagred3 --cov-report term-missing --cov-report xml

# Alias
tests: test

###########
# VERSION #
###########
.PHONY: show-version patch minor major

show-version:  ## show current library version
	@bump-my-version show current_version

patch:  ## bump a patch version
	@bump-my-version bump patch

minor:  ## bump a minor version
	@bump-my-version bump minor

major:  ## bump a major version
	@bump-my-version bump major

########
# DIST #
########
.PHONY: dist dist-build dist-sdist dist-local-wheel publish

dist-build:  # build python dists
	python -m build -w -s

dist-check:  ## run python dist checker with twine
	python -m twine check dist/*

dist: clean dist-build dist-check  ## build all dists

publish: dist  ## publish python assets

#########
# CLEAN #
#########
.PHONY: deep-clean clean

deep-clean: ## clean everything from the repository
	git clean -fdx

clean: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info

############################################################################################

.PHONY: help

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'
