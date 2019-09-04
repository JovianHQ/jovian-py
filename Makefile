.PHONY: export-env clean set-flavor set-flavor-pro build build-pro upload publish publish-pro 

export-env:
	conda env export > environment.yml --no-builds

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

publish-pro:
	make clean
	make build-pro
	make upload
