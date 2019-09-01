.PHONY: export-env clean build build-pro upload publish publish-pro

export-env:
	conda env export > environment.yml --no-builds

clean:
	trash ./*.egg-info
	trash ./dist
	trash ./build

build:
	PKG_NAME=jovian python setup.py sdist bdist_wheel

build-pro:
	PKG_NAME=jovian-pro python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

publish:
	make clean
	make build
	make upload

publish-pro:
	make clean
	make build-pro
	make upload

