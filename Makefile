VENV?=env

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test       to run unit tests"
	@echo "  build      to build the working virtual environment, and to install requirements for development"
	@echo "  clean      to remove the created virtualenv folder"

build: clean virtualenv requirements test-requirments

test: unittests

unittests:
	PYTHONPATH=$(CURDIR) nosetests -d -w tests -v

virtualenv:
	virtualenv $(CURDIR)/$(VENV)

clean:
	rm -rf $(CURDIR)/$(VENV)

requirements:
	$(CURDIR)/$(VENV)/bin/pip install -r requirements.txt

test-requirments:
	$(CURDIR)/$(VENV)/bin/pip install -r dev-requirements.txt