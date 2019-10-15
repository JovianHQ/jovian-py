.PHONY: help export-env clean set-flavor set-flavor-pro build build-pro upload publish publish-pro run-docs
VERSION:=`cat jovian/_version.py`

activate:
	conda activate jovian-pro-dev

help:
	echo "Check the Makefile for supported commands"

export-env:
	pip freeze > requirements.txt

clean:
	trash ./*.egg-info
	trash ./dist
	trash ./build

set-flavor:
	echo '__flavor__ = "jovian"' > ./jovian/_flavor.py

set-flavor-pro:
	echo '__flavor__ = "jovian-pro"' > ./jovian/_flavor.py

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