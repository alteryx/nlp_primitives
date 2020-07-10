.PHONY : entry-point-test lint-fix lint-tests unit-tests

entry-point-test:
	python -c "from featuretools import nlp_primitives"

lint-fix:
	select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221"
	autopep8 --in-place --recursive --max-line-length=100 --select=${select} nlp_primitives
	isort --recursive nlp_primitives

lint-tests:
	flake8 nlp_primitives
	isort --check-only nlp_primitives

unit-tests:
	pytest --cache-clear --show-capture=stderr -vv
