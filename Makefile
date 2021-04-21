PACKAGE := $(shell grep '^name =' setup.cfg | cut -d '=' -f2 | sed 's/ //g')
VERSION := $(shell head -n 1 $(PACKAGE)/assets/VERSION)

install:
	pip install --upgrade -e .
	test -f '.git/hooks/pre-commit' || cp .gitverify .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

dev:
	python3 -m pip install -e .

build:
	python3 -m pip install --upgrade build
	python3 -m build

lint:
	#black $(PACKAGE) tests --check
	pylama $(PACKAGE) tests

test:
	make lint
	pytest --cov ${PACKAGE} --cov-report term-missing --cov-fail-under 70 --cov-report=xml

test-ci:
	make lint
	pytest --cov ${PACKAGE} --cov-report term-missing --cov-fail-under 80 --ci