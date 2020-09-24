.PHONY : entry-point-test lint-fix lint-tests unit-tests

entry-point-test:
	python -c "from featuretools import nlp_primitives"

.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./nlp_primitives.egg-info

.PHONY: lint-fix
lint-fix:
	select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221"
	autopep8 --in-place --recursive --max-line-length=100 --select=${select} nlp_primitives
	isort --recursive nlp_primitives

.PHONY: lint-tests
lint-tests:
	flake8 nlp_primitives
	isort --check-only nlp_primitives

.PHONY: unit-tests
unit-tests:
	pytest --cache-clear --show-capture=stderr -vv

.PHONY: installdeps
installdeps:
	pip install --upgrade pip
	pip install -e .
	pip install -r test-requirements.txt
