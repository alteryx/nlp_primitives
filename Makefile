.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete

.PHONY: lint
lint:
	flake8 nlp_primitives && isort --check-only --recursive nlp_primitives

.PHONY: lint-fix
lint-fix:
	autopep8 --in-place --recursive --max-line-length=100 --select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221" nlp_primitives
	isort --recursive nlp_primitives

.PHONY: test
test:
	pytest nlp_primitives/tests

.PHONY: testcoverage
testcoverage: lint
	pytest nlp_primitives/tests --cov=nlp_primitives

.PHONY: installdeps
installdeps:
	pip install --upgrade pip -q
	pip install -e . -q
	pip install -r dev-requirements.txt -q