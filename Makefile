.PHONY : entry-point-test
entry-point-test:
	python -c "from featuretools import nlp_primitives"
	python -c "from featuretools.nlp_primitives import Elmo"
	python -c "from featuretools.primitives import Elmo"
	python -c "from nlp_primitives import Elmo"

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

.PHONY: lint
lint:
	flake8 nlp_primitives
	isort --check-only nlp_primitives

.PHONY: test
test:
	pytest --cache-clear --show-capture=stderr -vv

.PHONY: installdeps
installdeps:
	pip install --upgrade pip
	pip install -e .

.PHONY: installdeps-complete
installdeps-complete:
	pip install --upgrade pip
	pip install -e ".[complete]"

.PHONY: installdeps-test
installdeps-test:
	pip install --upgrade pip
	pip install -e ".[test]"

.PHONY: checkdeps
checkdeps:
	$(eval allow_list='featuretools|nltk')
	pip freeze | grep -v "nlp_primitives.git" | grep -E $(allow_list) > $(OUTPUT_FILEPATH)

.PHONY: checkdepscomplete
checkdepscomplete:
	$(eval allow_list='featuretools|nltk|tensorflow|tensorflow_hub')
	pip freeze | grep -v "nlp_primitives.git" | grep -E $(allow_list) > $(OUTPUT_FILEPATH)

.PHONY: upgradepip
upgradepip:
	python -m pip install --upgrade pip

.PHONY: upgradebuild
upgradebuild:
	python -m pip install --upgrade build

.PHONY: package_nlp_primitives
package_nlp_primitives: upgradepip upgradebuild
	python setup.py sdist
	$(eval PACKAGE=$(shell python setup.py --version))
	tar -zxvf "dist/nlp_primitives-${PACKAGE}.tar.gz"
	mv "nlp_primitives-${PACKAGE}" unpacked_sdist
