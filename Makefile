#!/usr/bin/make

test:
	make -C tests

ci-test:
	tests/test.sh

test-deploy:
	rm -fR build dist
	python3 setup.py sdist bdist_wheel --universal && twine upload -r testpypi dist/*
	pip  install --user flake8_tensors --index-url https://test.pypi.org/simple/
	pip uninstall flake8_tensors

deploy:
	rm -fR build dist
	python3 setup.py sdist bdist_wheel --universal && twine upload -r pypi dist/*
	`python -c 'import flake8_tensors; print(f"git tag -a v{flake8_tensors.__version__} -m release_{flake8_tensors.__version__}")'`
	git push --tags

update-test:
	rm -f test/reference.report
	flake8 test.py --select WT --output-file test/reference.report --exit-zero
