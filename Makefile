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
	rm -rf ./unpacked_sdist

.PHONY: lint
lint:
	isort --check-only nlp_primitives
	black nlp_primitives -t py310 --check
	flake8 nlp_primitives

.PHONY: lint-fix
lint-fix:
	black -t py310 nlp_primitives
	isort nlp_primitives

.PHONY: test
test:
	pytest nlp_primitives/ --cache-clear --show-capture=stderr -vv

.PHONY: testcoverage
testcoverage:
	pytest nlp_primitives/ --cov=nlp_primitives

.PHONY: installdeps
installdeps: upgradepip
	pip install -e ".[dev]"
	pre-commit run

.PHONY: installdeps-test
installdeps-test: upgradepip
	pip install -e ".[test]"

.PHONY: installdeps-complete
installdeps-complete: upgradepip
	pip install -e ".[complete]"

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

.PHONY: upgradesetuptools
upgradesetuptools:
	python -m pip install --upgrade setuptools

.PHONY: package
package: upgradepip upgradebuild upgradesetuptools
	python -m build
	$(eval PACKAGE=$(shell python -c "from pep517.meta import load; metadata = load('.'); print(metadata.version)"))
	tar -zxvf "dist/nlp_primitives-${PACKAGE}.tar.gz"
	mv "nlp_primitives-${PACKAGE}" unpacked_sdist
