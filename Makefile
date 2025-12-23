#!/usr/bin/make

test:
	make -C tests

ci-test:
	tests/test.sh

test-deploy:
	rm -fR build dist
	uv build && uvx twine upload -r testpypi dist/*
	pip  install --user flake8_tensors --index-url https://test.pypi.org/simple/ --verbose
	pip uninstall flake8_tensors

deploy:
	rm -fR build dist
	uv build && uvx twine upload --verbose -r pypi dist/*
	`uv run python -c 'import flake8_tensors; print(f"git tag -a v{flake8_tensors.__version__} -m release_{flake8_tensors.__version__}")'`
	git push --tags

update-test:
	rm -f test/reference.report
	uvx --from . flake8 test.py --select WT --output-file test/reference.report --exit-zero
