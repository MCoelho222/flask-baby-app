.PHONY: coverage build-docs

coverage:
	coverage erase && coverage run -m pytest tests/ && coverage report

build-docs:
	cd docs; make clean html
