.PHONY: all install lint release test test-ci

PACKAGE := $(shell grep '^name =' setup.cfg | cut -d '=' -f2 | sed 's/ //g')
VERSION := $(shell head -n 1 $(PACKAGE)/assets/VERSION)

install:
	pip install --upgrade -e .[dev]
	test -f '.git/hooks/pre-commit' || cp .gitverify .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

dev:
	python3 -m pip install -e .

build:
	python3 -m pip install --upgrade build
	python3 -m build

lint:
	pylama $(PACKAGE) tests

release:
	git checkout main && git pull origin && git fetch -p
	@git log --pretty=format:"%C(yellow)%h%Creset %s%Cgreen%d" --reverse -20
	@echo "\nReleasing v$(VERSION) in 10 seconds.\nDid you bump $(PACKAGE)/assets/VERSION and updated CHANGELOG.md?\nPress <CTRL+C> to abort\n" && sleep 10
	git commit -a -m 'v$(VERSION)' && git tag -a v$(VERSION) -m 'v$(VERSION)'
	git push --follow-tags

test:
	make lint
	pytest --cov ${PACKAGE} --cov-report term-missing --cov-fail-under 70 --cov-report=xml

test-ci:
	make lint
	pytest --cov ${PACKAGE} --cov-report term-missing --cov-fail-under 80 --ci