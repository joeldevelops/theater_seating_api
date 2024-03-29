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
	@hypercorn src:app --bind 0.0.0.0:8080 --log-level=debug --workers=4

start-dev:
	@export QUART_APP=src
	@quart run

venv:
	@virtualenv venv
	@source venv/bin/activate

install:
	@pip install -r requirements/common.txt

develop:
	@pip install -r requirements/common.txt -r requirements/develop.txt

init-db:
	@docker exec theater_seating_api-theater_seating-1 quart initdb

test:
	@pytest tests

load-test:
	@locust -f tests/load/locustfiles/api.py
