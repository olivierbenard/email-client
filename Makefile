.PHONY: run
run:
	poetry run python email_client/client.py

.PHONY: ruff
ruff:
	poetry run ruff check --select I --fix & \
	poetry run ruff format email_client/

.PHONY: mypy
mypy:
	poetry run mypy email_client/

.PHONY: pylint
pylint:
	poetry run pylint email_client/

.PHONY: tests
tests:
	poetry run pytest -vvs tests/

.PHONY: test-coverage
test-coverage:
	poetry run pytest --cov=email_client --cov-branch --cov-report=term-missing --cov-fail-under=90

.PHONY: checks
checks: ruff mypy pylint tests test-coverage

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
