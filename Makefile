help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test       to run unit tests"
	@echo "  build      to install requirements for development"

build: requirements test-requirements

test: unittests

unittests:
	PYTHONPATH=$(CURDIR) nosetests -d -w tests -v --with-coverage --cover-package ./crossengage

requirements:
	pip install -r requirements.txt

test-requirements:
	pip install -r test-requirements.txt