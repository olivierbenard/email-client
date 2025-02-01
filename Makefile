.PHONY: tests test-coverage

run:
	poetry run python email_client/client.py

black:
	poetry run black .

mypy:
	poetry run mypy email_client/

pylint:
	poetry run pylint email_client/

tests:
	poetry run pytest -vvs tests/

test-coverage:
	poetry run pytest --cov=email_client --cov-branch --cov-report=term-missing --cov-fail-under=90

checks: black mypy pylint tests test-coverage

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
