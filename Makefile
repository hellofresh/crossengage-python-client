help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test       to run unit tests"
	@echo "  setup      to install requirements for development"
	@echo "  build      to create a build directory for deployment"

build:
	@printf "$(OK_COLOR)==> Building$(NO_COLOR)\n"
	@mkdir -p "${BUILD_DIR}"
	@for SOURCE in crossengage setup.py; do \
		cp -r "$${SOURCE}" "${BUILD_DIR}/$${SOURCE}"; \
	done

setup: clean virtualenv requirements test-requirements

test:
	tox

test-unit:
	. $(CURDIR)/env/bin/activate; \
	tox

virtualenv:
	virtualenv $(CURDIR)/env

clean:
	rm -rf $(CURDIR)/env

requirements:
	$(CURDIR)/env/bin/python setup.py develop

test-requirements:
	$(CURDIR)/env/bin/pip install tox
