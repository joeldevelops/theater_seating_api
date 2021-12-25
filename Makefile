.PHONY: style check-style start install develop test load-test
style:
	# apply opinionated styles
	@black src
	@isort src

	# tests are production code too!
	@black tests
	@isort tests

check-style:
	@black src --check
	@flake8 orion --count --show-source --statistics --ignore=E203,W503

start:
	@bash bin/run.sh

venv:
	@virtualenv venv
	@source venv/bin/activate

install:
	@pip install -r requirements/common.txt

develop:
	@pip install -r requirements/common.txt -r requirements/develop.txt

test:
	@pytest tests

load-test:
	@locust -f tests/load/locustfiles/api.py
