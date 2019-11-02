.PHONY: help export-env clean set-flavor vars set-flavor-pro build build-pro upload publish publish-pro run-docs echo-version bump bump-dev bump-patch bump-release sanity-check-dev sanity-check-release

.DEFAULT_GOAL := help

VERSION = $(shell python setup.py --version)

setup-env:
	conda create -n jovian-py-dev python=3.5 -y
	@echo "Run:\n\tconda activate jovian-py-dev\n\tpip install -r requirements.txt"

activate:
	conda activate jovian-pro-dev

help:
	@echo "Check the Makefile for supported commands"

export-env:
	pip freeze > requirements.txt

clean:
	trash ./*.egg-info
	trash ./dist
	trash ./build

set-flavor:
	@echo '__flavor__ = "jovian"' > ./jovian/_flavor.py

set-flavor-pro:
	@echo '__flavor__ = "jovian-pro"' > ./jovian/_flavor.py

build:
	make set-flavor
	PKG_NAME=jovian python setup.py sdist bdist_wheel

build-pro:
	make set-flavor-pro
	PKG_NAME=jovian-pro python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

publish:
	make clean
	make build
	make upload
	sh ./deployAlert.sh PUBLIC $(VERSION)

publish-pro:
	make clean
	make build-pro
	make upload
	sh ./deployAlert.sh PRO $(VERSION)

run-docs:
	cd docs && make html
	sphinx-autobuild docs docs/_build/html

run-tests:
	python -m unittest discover

## Version bumping

define new_version
	$(shell bumpversion $(1) --dry-run --list --allow-dirty | sed -n 's/^ *new_version *= *//p')
endef

show-version:
	@echo Current version: $(VERSION)

bump-patch:
	$(eval NEW_VERSION := $(call new_version,patch))
	bumpversion patch
	@echo Bump version: $(VERSION) → $(NEW_VERSION)

bump-dev:
	$(eval NEW_VERSION := $(call new_version,dev))
	bumpversion dev
	@echo Bump version: $(VERSION) → $(NEW_VERSION)

bump-release:
	$(eval NEW_VERSION := $(call new_version,release))
	bumpversion release
	@echo Bump version: $(VERSION) → $(NEW_VERSION)


bump: bump-patch ## alias to bump-patch

sanity-check-dev:
	@perl -le '$$_=shift; $$v="dev version: $$_"; /^\d+\.\d+\.\d+\.dev\d+$$/ ? print "Good $$v" : die "Bad $$v, expecting X.Y.Z.devN format"' $(VERSION)

sanity-check-release:
	@perl -le '$$_=shift; $$v="release version: $$_"; /^\d+\.\d+\.\d+$$/ ? print "Good $$v" : die "Bad $$v, expecting X.Y.Z format"' $(VERSION)
