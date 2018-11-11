help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test       to run unit tests"
	@echo "  build      to install requirements for development"

build: requirements requirements-tests

test: unittests

unittests:
	PYTHONPATH=$(CURDIR) py.test --cov=crossengage tests/

requirements:
	pip install -r requirements.txt

requirements-tests:
	pip install -r requirements-tests.txt